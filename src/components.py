import math as math
from loadconfig import *
from utils import dist, cmp
from utils import UP, RIGHT, DOWN, LEFT
from utils import num_buildingtype, TOWNHALL, HUT, CANNON
from utils import NOTSTARTED, INGAME, WON, LOST
from utils import xy, attack_region
from colorama import init as coloramaInit, Fore as FG, Back as BG, Style as ST

coloramaInit()

## TODO : make unit sprites for each
## TODO : correct collision fn and collision bounce back
## TODO : use dt

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
                char = self.grid[i//self.unitsize.x][j//self.unitsize.y][i%self.unitsize.x][j%self.unitsize.y]
                if char == ' ' :
                    dire = self.closestBuilding[i//self.unitsize.x][j//self.unitsize.y]["dist"]
                    dire = int(cmp(dire.x,0)*3 + cmp(dire.y,0))
                    char = "·↓↗→↘↖←↙↑"[dire]
                print( char + ST.RESET_ALL, end='' )
            print()

    def calcClosestBuilding (self) :
        ## TODO : use bfs to improve complexity
        def calcWeight (d) :
            return max( abs(d.x) , abs(d.y) )
        def isBetter (a,b) :
            if a["weight"] == b["weight"] :
                return abs(a["dist"].x)+abs(a["dist"].y) < abs(b["dist"].x)+abs(b["dist"].y)
            else :
                return a["weight"] < b["weight"]
        def ClosestFormat ( dis, building ) :
            return { "dist": dis, "building": building, "weight": calcWeight(dis) }
        for i in range(self.size.x) :
            for j in range(self.size.y) :
                self.closestBuilding[i][j] = {}
                for buildingtype in self.buildings :
                    for building in buildingtype :
                        if building.health > 0 :
                            tmpClosest = ClosestFormat( dist(i, j, building), building )
                            if self.closestBuilding[i][j] == {} or \
                                    isBetter( tmpClosest, self.closestBuilding[i][j] ) :
                                        self.closestBuilding[i][j] = tmpClosest

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

        self.closestBuilding = [ [ {} for _ in range(self.size.y) ] for _ in range(self.size.x) ]
        self.calcClosestBuilding()

        self.king = None
        self.barbarians = []

    def gameStart (self, location) :
        self.king = king(self.spawns[location], UP)
        return game.checkOver()

    def spawn_barbarian (self, location) :
        self.barbarians.append( barbarian(self.spawns[location]) )

    def isColliding ( self, sprite, structs=None ) :
        if structs == None :
            # buildings have more priorities than walls- so in attack_region, buildings will show up first
            structs = [ building for buildingtype in self.buildings for building in buildingtype ] + self.walls
        for struct in structs :
            if sprite.position.x + sprite.size.x <= struct.position.x or \
               sprite.position.x >= struct.position.x + struct.size.x or \
               sprite.position.y + sprite.size.y <= struct.position.y or \
               sprite.position.y >= struct.position.y + struct.size.y or \
               struct.health <= 0 :
                continue
            return struct
        return False

    def gameloop (self, dt) :
        self.print()
        for barbarian_ in self.barbarians :
            if barbarian_.health > 0 :
                barbarian_.attack()
                barbarian_.move(dt)
        for cannon_ in self.buildings[CANNON] :
            if cannon_.health > 0 :
                cannon_.shoot()
        return self.checkOver()
        
    def checkOver (self) :
        status = INGAME
        if self.king is None :
            status = NOTSTARTED
        elif all( barbarian_.health <= 0 for barbarian_ in self.barbarians ) and self.king.health <= 0 :
            status = LOST
        elif all( building.health <= 0 for buildingtype in self.buildings for building in buildingtype ) :
                status = WON
        return status

game = gameplay(display_size, display_unit_size, display_fps, ' ');


class building :

    def __init__ ( self, health, position, size, defchar ) :
        self.health = health
        self.maxhealth = health
        self.position = position
        self.size = size
        self.defchar = defchar
        self.unit = [ [ [ [ defchar for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]

    def attacked ( self, damage ) :
        self.health -= damage
        if self.health <= 0 :
            game.calcClosestBuilding()
            return game.checkOver()

    def print (self) :
        if self.health > 0:
            color = FG.GREEN
            if self.health < self.maxhealth * 0.2 :
                color = FG.RED
            elif self.health < self.maxhealth * 0.5 :
                color = FG.YELLOW
            for i in range(self.size.x):
                if self.position.x+i <= game.size.x :
                    for j in range(self.size.y):
                        if self.position.y+j <= game.size.y :
                            for ui in range(game.unitsize.x):
                                for uj in range(game.unitsize.y):
                                    game.grid[int(self.position.x+i)][int(self.position.y+j)][ui][uj] = color + self.unit[i][j][ui][uj] + ST.RESET_ALL


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
                return enemy.attacked(self.damage)


class wall (building) :

    def __init__ ( self, position ) :
        super().__init__( wall_maxhealth, position, wall_size, 'W' )


class troop :

    def __init__ (self, position, health, damage, speed, size, defchar) :
        self.position = position
        self.health = health
        self.maxhealth = health
        self.damage = damage
        self.speed = speed
        self.size = size
        self.defchar = defchar
        self.unit = [ [ [ [ defchar for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]

    def attacked ( self, damage ) :
        self.health = max(0, self.health-damage)
        return game.checkOver()

    def move (self, dt) :
        oldx , oldy = self.position.x , self.position.y
        closest = game.closestBuilding[int(oldx)][int(oldy)]
        if closest != {} :
            direction = closest["dist"]
            self.position.x += self.speed*dt * cmp(direction.x,0)
            self.position.y += self.speed*dt * cmp(direction.y,0)
            ctr = 0
            while game.isColliding(self) != False and ctr < 1000 :
                self.position.x = ( self.position.x + oldx ) / 2
                self.position.y = ( self.position.y + oldy ) / 2
                ctr += 1
            self.position.x = self.position.x % game.size.x
            self.position.y = self.position.y % game.size.y

    def print (self) :
        color = FG.CYAN
        if self.health <= 0 :
            color = FG.RED + ST.BRIGHT
        elif self.health < self.maxhealth * 0.2 :
            color = FG.MAGENTA
        elif self.health < self.maxhealth * 0.4 :
            color = FG.LIGHTRED_EX
        elif self.health < self.maxhealth * 0.6 :
            color = FG.LIGHTMAGENTA_EX
        elif self.health < self.maxhealth * 0.8 :
            color = FG.BLUE
        for i in range(self.size.x):
            if self.position.x+i <= game.size.x :
                for j in range(self.size.y):
                    if self.position.y+j <= game.size.y :
                        for ui in range(game.unitsize.x):
                            for uj in range(game.unitsize.y):
                                game.grid[int(self.position.x+i)][int(self.position.y+j)][ui][uj] = color + self.unit[i][j][ui][uj] + ST.RESET_ALL

class king (troop) :

    def __init__ ( self, position, direction ) :
        super().__init__( position, king_maxhealth, king_damage, king_speed, king_size, 'K' )
        self.direction = direction

    def attack ( self ) :
        regposx = self.position.x
        regposy = self.position.y
        regsizx = self.size.x
        regsizy = self.size.y
        if self.direction == UP :
            regposy -= 1
            regsizy = 1
        elif self.direction == LEFT :
            regposx -= 1
            regsizx = 1
        elif self.direction == DOWN :
            regposy += self.size.y
            regsizy = 1
        elif self.direction == RIGHT :
            regposx += self.size.x
            regsizx = 1
        else :
            raise RuntimeError("unknown direction")

        region = attack_region(
                xy(int(regposx) , int(regposy)),
                xy(int(regsizx) , int(regsizy))
        )
        attackee = game.isColliding(region)
        if attackee == False :
            return attackee
        return attackee.attacked( self.damage )

    def move (self, towards, dt) :
            oldx , oldy = self.position.x , self.position.y
            if towards == UP :
                self.position.y -= self.speed*dt
            elif towards == RIGHT :
                self.position.x += self.speed*dt
            elif towards == DOWN :
                self.position.y += self.speed*dt
            elif towards == LEFT :
                self.position.x -= self.speed*dt
            else :
                raise RuntimeError("unknown direction")
            ctr = 0
            while game.isColliding(self) != False and ctr < 1000 :
                self.position.x = ( self.position.x + oldx ) / 2
                self.position.y = ( self.position.y + oldy ) / 2
                ctr += 1
            self.position.x = self.position.x % game.size.x
            self.position.y = self.position.y % game.size.y
            self.direction = towards

class barbarian (troop) :

    def __init__ ( self, position, ) :
        super().__init__( position, barbarian_maxhealth, barbarian_damage, barbarian_speed, barbarian_size, 'b' )

    def attack (self) :
        # the region around the troop - the area that the troop can damage
        regposx = self.position.x - 1
        regposy = self.position.y - 1
        regsizx = self.size.x + 2
        regsizy = self.size.y + 2

        region = attack_region(
                xy(int(regposx) , int(regposy)),
                xy(int(regsizx) , int(regsizy))
        )
        # buildings have more priority than walls so they are checked first
        attackee = game.isColliding(region)
        if attackee == False :
            return attackee
        return attackee.attacked( self.damage )
