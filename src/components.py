import math as math
from loadconfig import *
from utils import dist
from utils import UP, RIGHT, DOWN, LEFT
from utils import num_buildingtype, TOWNHALL, HUT, CANNON
from utils import NOTSTARTED, INGAME, WON, LOST

## TODO : make unit sprites for each

class gameplay :

    def __init__ (self, size, unitsize, fps, bgchar ) :
        self.size = size
        self.unitsize = unitsize
        self.fps = fps
        self.defchar = bgchar

    def print (self) :
        self.grid = [ [ [ [ self.defchar for _ in range(self.unitsize.y) ] for _ in range(self.unitsize.x) ] for _ in range(self.size.y) ] for _ in range(self.size.x) ]
        for struct in [ building for buildingtype in self.buildings for building in buildingtype ] + self.walls :
            if struct.health > 0 :
                struct.print()
        for enemy in [ self.king ] + self.barbarians :
            if enemy != None :
                enemy.print()
        for j in range(self.size.y*self.unitsize.y):
            for i in range(self.size.x*self.unitsize.x):
                #print(i,j)
                print( self.grid[i//self.unitsize.x][j//self.unitsize.y][i%self.unitsize.x][j%self.unitsize.y], end='' )
            print()

    def calcClosestBuilding (self) :
        ## TODO : use bfs to improve complexity
        def calcWeight (d) :
            return max( abs(d.x) , abs(d.y) )
        def ClosestFormat ( dis, buildingtype, n ) :
            return { "dist": dis, "buildingtype": buildingtype, "n": n, "weight": calcWeight(dis) }
        for i in range(self.size.x) :
            for j in range(self.size.y) :
                self.closestBuilding[i][j] = None
                for buildingtype in self.buildings :
                    for idx,building in enumerate(buildingtype) :
                        if building.health > 0 :
                            newdist = dist(i, j, building)
                            if self.closestBuilding[i][j] == None or \
                                    calcWeight(newdist) < self.closestBuilding[i][j]["weight"] :
                                self.closestBuilding[i][j] = ClosestFormat( newdist, buildingtype, idx )

    def gameInit ( self, spawns, townhall_positions, hut_positions, cannon_positions, wall_positions ) :
        if len(spawns) != 3 :
            raise RuntimeError("incorrect num of spawns:", len(spawns))
        if len(townhall_positions) != 1 :
            raise RuntimeError("incorrect num of townhalls: ", len(townhall_positions))
        if len(hut_positions) < 5 :
            raise RuntimeError("too few huts:", len(hut_positions))
        if len(cannon_positions) < 2 :
            raise RuntimeError("too few cannons:", len(cannon_positions))

        self.spawns = spawns

        self.buildings = [ [] for _ in range(num_buildingtype) ]
        self.buildings[TOWNHALL] = [ townhall(pos) for pos in townhall_positions ]
        self.buildings[HUT] = [ hut(pos) for pos in hut_positions ]
        self.buildings[CANNON] = [ cannon(pos) for pos in cannon_positions ]
        self.walls = [ wall(pos) for pos in wall_positions ]

        self.closestBuilding = [ [ None for _ in range(self.size.y) ] for _ in range(self.size.x) ]
        self.calcClosestBuilding()

        self.king = None
        self.barbarians = []

    def gameStart (self, location) :
        self.king = king(self.spawns[location], UP)

    def spawn_barbarian (self, location) :
        self.barbarians.append( barbarian(self.spawns[location]) )

    def isColliding ( self, sprite ) :
        for struct in [ building for buildingtype in self.buildings for building in buildingtype ] + self.walls :
            if sprite.position.x + sprite.size.x <= struct.position.x or \
               sprite.position.x >= struct.position.x + struct.size.x or \
               sprite.position.y + sprite.size.y <= struct.position.y or \
               sprite.position.y >= struct.position.y + struct.size.y or \
               struct.health <= 0 :
                continue
            return False
        return True
        
    def endscreen (self,status) :
        ## TODO : make endscreens
        if status is WON :
            print("gg")
        elif status is LOST :
            print("better luck next time")

    def checkOver (self) :
        status = INGAME
        if self.king is None :
            status = NOTSTARTED
        elif all( barbarian_.health <= 0 for barbarian_ in self.barbarians ) and self.king.health <= 0 :
            status = LOST
        elif all( building.health <= 0 for buildingtype in self.buildings for building in buildingtype ) :
                status = WON
        self.endscreen(status)
        return status

game = gameplay(display_size, display_unit_size, display_fps, ' ');


class building :

    def __init__ ( self, health, position, size, defchar ) :
        self.health = health
        self.position = position
        self.size = size
        self.defchar = defchar
        self.unit = [ [ [ [ defchar for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]

    def attacked ( self, damage ) :
        self.health -= damage
        if self.health <= 0 :
            game.calcClosestBuilding()
            game.checkOver()

    def print (self) :
        if self.health > 0:
            for i in range(self.size.x):
                if self.position.x+i <= game.size.x :
                    for j in range(self.size.y):
                        if self.position.y+j <= game.size.y :
                            for ui in range(game.unitsize.x):
                                for uj in range(game.unitsize.y):
                                    game.grid[self.position.x+i][self.position.y+j][ui][uj] = self.unit[i][j][ui][uj]


class townhall (building) :

    def __init__ ( self, position ) :
        super().__init__( townhall_maxhealth, position, townhall_size, 'T' )


class hut (building) :

    def __init__ ( self, position ) :
        super().__init__( hut_maxhealth, position, hut_size, 'H' )


class cannon (building) :

    def __init__ ( self, position ) :
        super().__init__( cannon_maxhealth, position, cannon_size, 'C' )
        self.range = cannon_range
        self.damage = cannon_damage

    def shoot (self) :
        def inrange (pos) :
            # TODO : better inrange algorithm
            return abs(self.position.x-pos.x)+abs(self.position.y-pos.y) <= self.range
        for enemy in [ game.king ] + game.barbarians :
            if enemy != None and enemy.health > 0 and inrange ( enemy.position ) :
                enemy.attacked(self.damage)
                break


class wall (building) :

    def __init__ ( self, position ) :
        super().__init__( wall_maxhealth, position, wall_size, 'W' )


class troop :

    def __init__ (self, position, health, damage, speed, size, defchar) :
        self.position = position
        self.health = health
        self.damage = damage
        self.speed = speed
        self.size = size
        self.defchar = defchar
        self.unit = [ [ [ [ defchar for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]

    def attacked ( self, damage ) :
        self.health = max(0, self.health-damage)
        game.checkOver()

    def move (self) :
        closest = game.closestBuilding[self.position.x][self.position.y]
        if closest != None :
            direction = closest["dist"]
            newx = self.position.x + math.copysign(self.speed,direction.x)
            newy = self.position.y + math.copysign(self.speed,direction.y)
            while game.isColliding(self) :
                newx = ( self.position.x + newx ) / 2
                newy = ( self.position.y + newy ) / 2
            self.position.x , self.position.y = newx , newy

    def print (self) :
        for i in range(self.size.x):
            if self.position.x+i <= game.size.x :
                for j in range(self.size.y):
                    if self.position.y+j <= game.size.y :
                        for ui in range(game.unitsize.x):
                            for uj in range(game.unitsize.y):
                                game.grid[self.position.x+i][self.position.y+j][ui][uj] = self.unit[i][j][ui][uj]

class king (troop) :

    def __init__ ( self, position, direction ) :
        super().__init__( position, king_maxhealth, king_damage, king_speed, king_size, 'K' )
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
        for struct in [ building for buildingtype in game.buildings for building in buildingtype ] + game.walls :
            if struct.health > 0 and struct.position.x == nextx and struct.position.y == nexty :
                struct.attacked( self.damage )
                break

    def move (self, towards) :
            nextx , nexty = self.position.x , self.position.y
            if towards == UP :
                nexty -= self.speed
            elif towards == RIGHT :
                nextx += self.speed
            elif towards == DOWN :
                nexty += self.speed
            elif towards == LEFT :
                nextx -= self.speed
            else :
                raise RuntimeError("unknown direction")
            while game.isColliding(self) :
                nextx = ( self.position.x + nextx ) / 2
                nexty = ( self.position.y + nexty ) / 2
            self.position.x , self.position.y = nextx , nexty
            self.direction = towards

class barbarian (troop) :

    def __init__ ( self, position, ) :
        super().__init__( position, barbarian_maxhealth, barbarian_damage, barbarian_speed, barbarian_size, 'b' )

    def attack (self) :
        closest = game.closestBuilding[self.position.x][self.position.y]
        if closest != None :
            if closest.weight == 0 :
                # closest building must have more than 0 health
                game.buildings[closest.buildingtype][closest.n].attacked( self.damage )
            else :
                nextx , nexty = self.position.x + math.copysign(1,closest["dist"].x) , self.position.y + math.copysign(1,closest["dist"].y)
                for wall in game.walls :
                    if wall.health > 0 and wall.position.x == nextx and wall.position.y == nexty :
                        wall.attacked( self.damage )
