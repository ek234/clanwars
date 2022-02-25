import math as math
from loadconfig import *
from utils import dist
from utils import UP, RIGHT, DOWN, LEFT
from utils import TOWNHALL, HUT, CANNON

## TODO : push object out incase of collision
## TODO : avoid overlap of buildings

class gameplay :

    def __init__ (self, size, unitsize ) :
        self.size = size
        self.unitsize = unitsize
        self.grid = [ [ [ [ '=' for _ in range(unitsize.y) ] for _ in range(unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]

    def print (self) :
        ## print the self.grid (and translate the chars to ascii)
        for i in range(self.size.x):
            for j in range(self.size.y):
                for ui in range(self.unitsize.x):
                    for uj in range(self.unitsize.y):
                        # add translation here
                        print( self.grid[i][j][ui][uj] )

    def calcClosestBuilding (self) :
        ## TODO : use bfs to improve complexity
        def calcWeight (d) :
            return max( abs(d.x) , abs(d.y) )
        def ClosestFormat ( dis, buildingtype, n ) :
            return { "dist": dis, "buildingtype": buildingtype, "n": n, "weight": calcWeight(dis) }
        for i in range(self.size.x) :
            for j in range(self.size.y) :
                ## if no building exists, then townhall is the default (even if it does not exist)
                dis = dist(i, j, self.buildings[TOWNHALL])
                self.closestBuilding[i][j] = ClosestFormat( dis, TOWNHALL, 0 )
                for buildingtype in [ HUT, CANNON ] :
                    for i in range(len(self.buildings[buildingtype])):
                        newdist = dist(i, j, self.buildings[buildingtype][i])
                        if calcWeight(newdist) < self.closestBuilding[i][j].weight :
                        #if calcWeight(newdist) < self.closestBuilding[i][j]["weight"] :
                            self.closestBuilding[i][j] = ClosestFormat( newdist, buildingtype, i )

    def gameInit ( self, spawns, townhall_position, hut_positions, cannon_positions, wall_positions ) :
        self.spawns = spawns
        if len(self.spawns) != 3 :
            raise RuntimeError("wrong num of spawns:", len(self.spawns))
        self.buildings = [ [] for _ in range(4) ]
        self.buildings[TOWNHALL] = [ townhall( townhall_position ) ]
        self.buildings[HUT] = [ hut(pos) for pos in hut_positions ]
        if len(self.buildings[HUT]) < 5 :
            raise RuntimeError("too few huts:", len(self.buildings[HUT]))
        self.buildings[CANNON] = [ cannon(pos) for pos in cannon_positions ]
        if len(self.buildings[CANNON]) < 2 :
            raise RuntimeError("too few cannons:", len(self.buildings[CANNON]))
        self.walls = [ wall(pos) for pos in wall_positions ]
        self.closestBuilding = []
        self.calcClosestBuilding()
        self.barbarians = []

    def gameStart (self, location) :
        self.king = king(self.spawns[location], UP)

    def isColliding ( self, obj ) :
        for ele in [ building for buildingtype in self.buildings for building in buildingtype ] + self.walls :
            if obj.position.x + obj.size.x <= ele.position.x or \
               obj.position.x >= ele.position.x + ele.size.x or \
               obj.position.y + obj.size.y <= ele.position.y or \
               obj.position.y >= ele.position.y + ele.size.y :
                continue
            return False
        return True
        
    def checkOver (self) :
        return \
                all( building.health <= 0 for buildingtype in self.buildings for building in buildingtype ) or \
                ( all( barbarian_.health <= 0 for barbarian_ in self.barbarians) and \
                ( self.king != None and self.king.health <= 0 ) )

game = gameplay(display_size, display_unit_size);

class building :
    def __init__ ( self, health, position, size ) :
        self.health = health
        self.position = position
        self.size = size
        self.unit = [ [ [ [ 'b' for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]
    def attacked ( self, damage ) :
        self.health -= damage
        if self.health <= 0 :
            game.calcClosestBuilding()
            game.checkOver()
    def print (self) :
        if self.health > 0:
            for i in range(self.size.x):
                for j in range(self.size.y):
                    for ui in range(game.unitsize.x):
                        for uj in range(game.unitsize.y):
                            game.grid[self.position.x+i][self.position.y+j][ui][uj] = self.unit[i][j][ui][uj]

class townhall (building) :
    def __init__ ( self, position ) :
        super().__init__( townhall_maxhealth, position, townhall_size )

class hut (building) :
    def __init__ ( self, position ) :
        super().__init__( hut_maxhealth, position, hut_size )

class cannon (building) :
    def __init__ ( self, position ) :
        super().__init__( cannon_maxhealth, position, cannon_size )
        self.range = cannon_range
        self.damage = cannon_damage
    def shoot (self) :
        def inrange ( a, b ) :
            return abs(a.x-b.x)+abs(a.y-b.y) <= self.range
        for enemy in [ game.king, game.barbarians ] :
            if inrange ( self.position, enemy.position ) :
                enemy.attacked(self.damage)
                break

class wall (building) :
    def __init__ ( self, position ) :
        super().__init__( wall_maxhealth, position, wall_size )

class troop :
    def __init__ (self, position, health, damage, speed, size) :
        self.position = position
        self.health = health
        self.damage = damage
        self.speed = speed
        self.size = size
        self.unit = [ [ [ [ 't' for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]
    def attack (self) :
        closest = game.closestBuilding[self.position.x][self.position.y]
        if closest.weight == 0 :
            game.buildings[closest.buildingtype][closest.n].attacked( self.damage )
        else :
            nextx , nexty = self.position.x + math.copysign(1,closest.dist.x) , self.position.y + math.copysign(1,closest.dist.y)
            for wall in game.walls :
                if ( wall.position.x == nextx and wall.position.y == nexty ) :
                    wall.attacked( self.damage )
    def attacked ( self, damage ) :
        self.health = max(0, self.health-damage)
        game.checkOver()
    def move (self) :
        direction = game.closestBuilding[self.position.x][self.position.y].dist
        newx , newy = self.position.x + math.copysign(self.speed,direction.x) , self.position.y + math.copysign(self.speed,direction.y)
        #if not any( wall.position.x == newx and wall.position.y == newy for wall in game.walls ):
        if game.isColliding(self) == False :
            self.position.x , self.position.y = newx , newy
    def print (self) :
        for i in range(self.size.x):
            for j in range(self.size.y):
                for ui in range(game.unitsize.x):
                    for uj in range(game.unitsize.y):
                        game.grid[self.position.x][self.position.y][ui][uj] = self.unit[i][j][ui][uj]

class king (troop) :
    def __init__ ( self, position, direction ) :
        super().__init__( position, king_maxhealth, king_damage, king_speed, king_size )
        self.direction = direction
    def attack ( self ) :
            nextx,nexty = self.position.x,self.position.y
            if self.direction == UP :
                nexty -= 1
            elif self.direction == RIGHT :
                nextx += 1
            elif self.direction == DOWN :
                nexty += 1
            elif self.direction == LEFT :
                nextx -= 1
            else :
                raise RuntimeError("unknown direction")

            for wall in game.walls :
                if ( wall.position.x == nextx and wall.position.y == nexty ) :
                    wall.attacked( self.damage )
            for buildingtype in game.buildings :
                for building in buildingtype :
                    if ( building.position.x == nextx and building.position.y == nexty ) :
                        building.attacked( self.damage )

class barbarian (troop) :
    def __init__ ( self, position, ) :
        super().__init__( position, barbarian_maxhealth, barbarian_damage, barbarian_speed, barbarian_size )
    def spawn (self, location) :
        game.barbarians.append( barbarian(game.spawns[location]) )
