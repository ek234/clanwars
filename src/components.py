from copy import copy as cp
from loadconfig import *
from utils import dist, cmp
from utils import UP, RIGHT, DOWN, LEFT
from utils import num_buildingtype, TOWNHALL, HUT, CANNON
from utils import NOTSTARTED, INGAME, WON, LOST
from utils import XY, AttackRegion
from sprites import townhall_unit, hut_unit, cannon_unit, wall_unit, barbarian_unit, king_unit, archer_unit, ballon_unit
from colorama import init as coloramaInit, Fore as FG, Back as BG, Style as ST, ansi
from random import random as rnd
from random import seed

DEBUG = False

coloramaInit()

class Gameplay :

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
        for enemy in [ self.king ] + self.barbarians + self.archers + self.ballons :
            if enemy != None :
                enemy.print()

        # clear screen
        toprint = ansi.clear_screen()
        for j in range(self.size.y*self.unitsize.y):
            for i in range(self.size.x*self.unitsize.x):
                char = self.grid[i//self.unitsize.x][j//self.unitsize.y][i%self.unitsize.x][j%self.unitsize.y]
                if char == ' ' and self.closestBuilding[i//self.unitsize.x][j//self.unitsize.y] != {} and DEBUG :
                    dire = self.closestBuilding[i//self.unitsize.x][j//self.unitsize.y]["dist"]
                    dire = int(cmp(dire.x,0)*3 + cmp(dire.y,0))
                    char = "·↓↗→↘↖←↙↑"[dire]
                toprint += char + ST.RESET_ALL
            if j == self.size.y // 4 :
                if self.king != None :
                    toprint += "king's health: " + str(self.king.health)
            if j == self.size.y // 4 + 1:
                if self.king != None :
                    toprint += "weapon:"
                    if self.king.isAxe :
                        toprint += "axe"
                    else :
                        toprint += "sword"
            if j == self.size.y // 2 :
                toprint += "Keybinds:"
            if j == self.size.y // 2 + 1 :
                toprint += "1/2/3: spawn"
            if j == self.size.y // 2 + 2 :
                toprint += "w/a/s/d: king"
            if j == self.size.y // 2 + 3 :
                toprint += "e: change weapon"
            if j == self.size.y // 2 + 4 :
                toprint += "<space>: attack"
            if j == self.size.y // 2 + 5 :
                toprint += "x: heal"
            if j == self.size.y // 2 + 6 :
                toprint += "c: rage"
            if j == self.size.y // 2 + 7 :
                toprint += "z: rise"
            if j == self.size.y // 2 + 8 :
                toprint += "[: quit"
            toprint += "\n"
        print( toprint )

    def calcClosestBuilding (self) :
        ## todo : use bfs to improve complexity
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
                self.closestAggressive[i][j] = {}
                for buildingtype in self.buildings :
                    for building in buildingtype :
                        if building.health > 0 :
                            tmpClosest = ClosestFormat( dist(i, j, building), building )
                            if self.closestBuilding[i][j] == {} or \
                                    isBetter( tmpClosest, self.closestBuilding[i][j] ) :
                                        self.closestBuilding[i][j] = tmpClosest
                            # TODO : add wizzard tower here too
                            if building.__class__.__name__ in { "Cannon" } and \
                               ( self.closestAggressive[i][j] == {} or \
                                    isBetter( tmpClosest, self.closestAggressive[i][j] ) ) :
                                        self.closestAggressive[i][j] = tmpClosest

    def gameInit ( self, spawns, townhall_positions, hut_positions, cannon_positions, wall_positions, seed_ ) :

        seed(seed_)
        
        if len(spawns) != 3 :
            raise RuntimeError("incorrect num of spawns:", len(spawns))
        if len(townhall_positions) != 1 :
            raise RuntimeError("incorrect num of townhalls: ", len(townhall_positions))
        if len(hut_positions) < 5 :
            raise RuntimeError("too few huts:", len(hut_positions))
        if len(cannon_positions) < 2 :
            raise RuntimeError("too few cannons:", len(cannon_positions))
        if 2*archer_maxhealth != barbarian_maxhealth or 2*archer_damage != barbarian_damage or archer_speed != 2*barbarian_speed :
            raise RuntimeError("archer config error")
        if ballon_maxhealth != barbarian_maxhealth or ballon_damage != 2*barbarian_damage or ballon_speed != 2*barbarian_speed :
            raise RuntimeError("ballon config error")

        self.spawns = spawns

        self.buildings = [ [] for _ in range(num_buildingtype) ]
        self.buildings[TOWNHALL] = [ Townhall(pos) for pos in townhall_positions ]
        self.buildings[HUT] = [ Hut(pos) for pos in hut_positions ]
        self.buildings[CANNON] = [ Cannon(pos) for pos in cannon_positions ]
        self.walls = [ Wall(pos) for pos in wall_positions ]

        self.closestBuilding = [ [ {} for _ in range(self.size.y) ] for _ in range(self.size.x) ]
        self.closestAggressive = [ [ {} for _ in range(self.size.y) ] for _ in range(self.size.x) ]
        self.calcClosestBuilding()

        self.king = None
        self.barbarians = []
        self.archers = []
        self.ballons = []

        self.TimeToRage = 0

    def gameStart (self, location) :
        self.king = King(self.spawns[location], UP)
        return game.checkOver()

    def spawn (self, location) :
        if location // 3 == 0 :
            self.barbarians.append( Barbarian(self.spawns[location]) )
        elif location // 3 == 1 :
            self.archers.append( Archer(self.spawns[location%3]) )
        elif location // 3 == 2 :
            self.ballons.append( Ballon(self.spawns[location%3]) )
        else :
            print("hmm")
            return

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
        self.TimeToRage = max( self.TimeToRage-dt, 0 )
        for troop in self.barbarians + self.archers + self.ballons :
            if troop.health > 0 :
                troop.attack() # can it attack and move?
                troop.move(dt)
        for cannon_ in self.buildings[CANNON] :
            if cannon_.health > 0 :
                cannon_.shoot()
        self.print()
        return self.checkOver()
        
    def spell_heal ( self ) :
        for enemy in [ game.king ] + game.barbarians + game.archers + game.ballons :
            if enemy != None :
                if enemy.health > 0 :
                    enemy.health = min( int( enemy.health * 1.5 ) , enemy.maxhealth )

    def spell_rage ( self ) :
        self.TimeToRage = rage_timecap

    def spell_rise ( self ) :
        for enemy in [ self.king ] + self.barbarians + game.archers + game.ballons :
            if enemy != None :
                if enemy.health <= 0 :
                    enemy.health = enemy.maxhealth * 0.1

    def checkOver (self) :
        status = INGAME
        if self.king is None :
            status = NOTSTARTED
        elif all( troop.health <= 0 for troop in self.barbarians + self.archers + self.ballons ) and self.king.health <= 0 :
            status = LOST       # TODO show lost status only when all troops have been deployed
        elif all( building.health <= 0 for buildingtype in self.buildings for building in buildingtype ) :
            status = WON
        return status

game = Gameplay(display_size, display_unit_size, display_fps, ' ');

class Building :

    def __init__ ( self, health, position, size, defchar, unit=None ) :
        self.health = health
        self.maxhealth = health
        self.position = cp(position)
        self.size = cp(size)
        self.defchar = defchar
        self.wasHurt = False
        if unit == None :
            self.unit = [ [ [ [ defchar for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]
        else :
            self.unit = unit

    def attacked ( self, damage ) :
        self.health -= damage
        if self.health <= 0 :
            game.calcClosestBuilding()
        self.wasHurt = True
        return game.checkOver()

    def print (self) :
        if self.health > 0:
            color = FG.GREEN
            if self.health < self.maxhealth * 0.2 :
                color = FG.RED
            elif self.health < self.maxhealth * 0.5 :
                color = FG.YELLOW
            if self.wasHurt :
                self.wasHurt = False
                # color = FG.BLACK
            if self.__class__.__name__ == "Cannon" and self.justShot :
                self.justShot = False
                color += BG.WHITE
            for i in range(self.size.x):
                if self.position.x+i <= game.size.x :
                    for j in range(self.size.y):
                        if self.position.y+j <= game.size.y :
                            for ui in range(game.unitsize.x):
                                for uj in range(game.unitsize.y):
                                    game.grid[int(self.position.x+i)][int(self.position.y+j)][ui][uj] = color + self.unit[i][j][ui][uj] + ST.RESET_ALL


class Townhall (Building) :

    def __init__ ( self, position ) :
        super().__init__( townhall_maxhealth, position, townhall_size, 'T', townhall_unit )


class Hut (Building) :

    def __init__ ( self, position ) :
        super().__init__( hut_maxhealth, position, hut_size, 'H', hut_unit )


class Cannon (Building) :

    def __init__ ( self, position ) :
        super().__init__( cannon_maxhealth, position, cannon_size, 'C', cannon_unit )
        self.range = cp(cannon_range)
        self.damage = cp(cannon_damage)
        self.justShot = False

    def shoot (self) :
        def inrange (pos) :
            return abs(self.position.x-pos.x)+abs(self.position.y-pos.y) <= self.range
        for enemy in [ game.king ] + game.barbarians + game.archers + game.ballons :
            if enemy != None and enemy.health > 0 and inrange ( enemy.position ) :
                self.justShot = True
                return enemy.attacked(self.damage)


class Wall (Building) :

    def __init__ ( self, position ) :
        super().__init__( wall_maxhealth, position, wall_size, 'W', wall_unit )


class Troop :

    def __init__ ( self, position, health, damage, speed, size, defchar, unit=None ) :
        self.position = cp(position)
        self.health = health
        self.maxhealth = health
        self.damage = damage
        self.speed = speed * ( 1 + rnd()/8 )
        self.size = cp(size)
        self.defchar = defchar
        self.wasHurt = False
        if unit == None :
            self.unit = [ [ [ [ defchar for _ in range(game.unitsize.y) ] for _ in range(game.unitsize.x) ] for _ in range(size.y) ] for _ in range(size.x) ]
        else :
            self.unit = unit

    def attacked ( self, damage ) :
        self.health = max(0, self.health-damage)
        self.wasHurt = True
        return game.checkOver()

    def move (self, dt) :
        def moveOnce ( ds ) :
            closest = game.closestBuilding[int(self.position.x)][int(self.position.y)]
            if closest != {} :
                direction = closest["dist"]

                # assert game.isColliding(self) == False

                self.position.x += cmp(direction.x,0) * ds
                if game.isColliding(self) != False :
                    self.position.x = int(self.position.x)
                    if game.isColliding(self) != False :
                        self.position.x -= cmp(direction.x,0)

                self.position.y += cmp(direction.y,0) * ds
                if game.isColliding(self) != False :
                    self.position.y = int(self.position.y)
                    if game.isColliding(self) != False :
                        self.position.y -= cmp(direction.y,0)

        if self.health > 0 :
            dist = self.speed * dt
            if game.TimeToRage > 0 :
                dist *= 2

            moveOnce(dist - int(dist))
            for _ in range(int(dist)) :
                moveOnce(1)

    def print (self) :
        color = FG.CYAN
        if self.health <= 0 :
            color = FG.RED + ST.BRIGHT
        elif self.health < self.maxhealth * 0.2 :
            color = FG.LIGHTRED_EX
        elif self.health < self.maxhealth * 0.4 :
            color = FG.LIGHTMAGENTA_EX
        elif self.health < self.maxhealth * 0.6 :
            color = FG.BLUE
        elif self.health < self.maxhealth * 0.8 :
            color = FG.LIGHTCYAN_EX
        if self.wasHurt :
            self.wasHurt = False
            # color = FG.BLACK
        if game.TimeToRage > 0 and self.health > 0 :
            color += BG.YELLOW
        for i in range(self.size.x):
            if self.position.x+i <= game.size.x :
                for j in range(self.size.y):
                    if self.position.y+j <= game.size.y :
                        for ui in range(game.unitsize.x):
                            for uj in range(game.unitsize.y):
                                game.grid[int(self.position.x+i)][int(self.position.y+j)][ui][uj] = color + self.unit[i][j][ui][uj] + ST.RESET_ALL

class King (Troop) :

    def __init__ ( self, position, direction ) :
        super().__init__( position, king_maxhealth, king_damage, king_speed, king_size, 'K', king_unit )
        self.direction = direction
        self.isAxe = True
        self.axeRange = king_axeRange

    def attack ( self ) :
        if self.health > 0 :
            attackees = set()

            if self.isAxe :
                # manhattan distance
                for x in range(-self.axeRange, self.axeRange+1) :
                    for y in range(-(self.axeRange - abs(x)), (self.axeRange - abs(x))+1) :
                        region = AttackRegion(
                                XY(int(self.position.x)+x,int(self.position.y)+y),
                                XY(1,1)
                        )
                        attackee = game.isColliding(region)
                        if attackee != False :
                            attackees.add(attackee)

            else :
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

                region = AttackRegion(
                        XY(int(regposx) , int(regposy)),
                        XY(int(regsizx) , int(regsizy))
                )
                attackee = game.isColliding(region)
                if attackee != False :
                    attackees.add(attackee)

            if len(attackees) == 0 :
                return False

            damage = self.damage
            if game.TimeToRage > 0 :
                damage *= 2

            attacked = []
            for attackee in attackees :
                attacked.append( attackee.attacked( damage ) )
            return attacked
        return False

    def move (self, towards, dt) :
        def moveOnce ( dx, dy, ds ) :
            # assert game.isColliding(self) == False

            if dx != 0 :
                self.position.x += cmp(dx,0) * ds
                if game.isColliding(self) != False :
                    self.position.x = int(self.position.x)
                    if game.isColliding(self) != False :
                        self.position.x -= cmp(dx,0)

            if dy != 0 :
                self.position.y += cmp(dy,0) * ds
                if game.isColliding(self) != False :
                    self.position.y = int(self.position.y)
                    if game.isColliding(self) != False :
                        self.position.y -= cmp(dy,0)

        if self.health > 0 :

            speed = self.speed
            if game.TimeToRage > 0 :
                speed *= 2
            dis = speed * dt

            dx,dy = 0,0
            if towards == UP :
                dy -= speed*dt
            elif towards == LEFT :
                dx -= dis
            elif towards == DOWN :
                dy += dis
            elif towards == RIGHT :
                dx += dis
            else :
                raise RuntimeError("unknown direction")

            self.direction = towards
            moveOnce( dx, dy, dis - int(dis) )
            for _ in range(int(dis)) :
                moveOnce( dx, dy, 1 )

class Barbarian (Troop) :

    def __init__ ( self, position ) :
        super().__init__( position, barbarian_maxhealth, barbarian_damage, barbarian_speed, barbarian_size, 'b', barbarian_unit )

    def attack (self) :
        if self.health > 0 :
            closest = game.closestBuilding[int(self.position.x)][int(self.position.y)]
            if closest != {} :
                direction = closest["dist"]
                regposx = self.position.x
                regposy = self.position.y
                regsizx = self.size.x
                regsizy = self.size.y
                if direction.x < 0 :
                    regposx -= 1
                    regsizx = 1
                elif direction.x > 0 :
                    regposx += self.size.x
                    regsizx = 1
                if direction.y < 0 :
                    regposy -= 1
                    regsizy = 1
                elif direction.y > 0 :
                    regposy += self.size.y
                    regsizy = 1

                region = AttackRegion(
                        XY(int(regposx) , int(regposy)),
                        XY(int(regsizx) , int(regsizy))
                )

                # buildings have more priority than walls so they are checked first
                attackee = game.isColliding(region)
                if attackee == False :
                    return False
                damage = self.damage
                if game.TimeToRage > 0 :
                    damage *= 2
                return attackee.attacked( damage )
        return False

class Archer (Troop) :

    def __init__ ( self, position ) :
        super().__init__( position, archer_maxhealth, archer_damage, archer_speed, archer_size, 'a', archer_unit )
        self.range = archer_range

    def attack (self) :
        if self.health > 0 :
            damage = self.damage
            if game.TimeToRage > 0 :
                damage *= 2
            def inrange (pos) :
                return abs(self.position.x-pos.x)+abs(self.position.y-pos.y) <= self.range
            for struct in [ building for buildingtype in game.buildings for building in buildingtype ] + game.walls :
                if struct != None and struct.health > 0 and inrange ( struct.position ) :
                    return struct.attacked(damage)
        return False

class Ballon (Troop) :

    def __init__ ( self, position, ) :
        super().__init__( position, ballon_maxhealth, ballon_damage, ballon_speed, ballon_size, 'a', ballon_unit )

    def attack (self) :
        if self.health > 0 :
            attackee = False
            if game.closestAggressive[int(self.position.x)][int(self.position.y)] == {} :
                attackee = game.isColliding(self, game.buildings[TOWNHALL]+game.buildings[HUT])
            else :
                # TODO : add wiz tower
                attackee = game.isColliding(self, game.buildings[CANNON])
            if attackee == False :
                return False

            damage = self.damage
            if game.TimeToRage > 0 :
                damage *= 2
            return attackee.attacked( damage )
        return False

    def move (self, dt) :
        def moveOnce ( ds ) :
            closest = game.closestAggressive[int(self.position.x)][int(self.position.y)]
            if closest == {} :
                closest = game.closestBuilding[int(self.position.x)][int(self.position.y)]

            if closest != {} :
                direction = closest["dist"]

                self.position.x += cmp(direction.x,0) * ds
                self.position.y += cmp(direction.y,0) * ds

        if self.health > 0 :
            dist = self.speed * dt
            if game.TimeToRage > 0 :
                dist *= 2

            moveOnce(dist - int(dist))
            for _ in range(int(dist)) :
                moveOnce(1)
