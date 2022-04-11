num_buildingtype = 4
num_spells = 2

CHANGE_WEAPON = 'e'
CHANGE_WEAPON = '.'

UP, LEFT, DOWN, RIGHT = 'w', 'a', 's', 'd'
UP, LEFT, DOWN, RIGHT = ',', 'a', 'o', 'e'

SPELL_RAGE, SPELL_HEAL, SPELL_RISE = 'c', 'x', 'z'
SPELL_RAGE, SPELL_HEAL, SPELL_RISE = 'j', 'q', ';'

# enum
TOWNHALL, HUT, CANNON, TOWER = range(num_buildingtype)
NOTSTARTED, INGAME, WON, LOST = range(-1,3)

class XY :
    def __init__ (self, x, y) :
        self.x = x
        self.y = y

class AttackRegion :
    def __init__ (self, position, size) :
        self.position = position
        self.size = size

def cmp(a, b):
    return (a > b) - (a < b)

def dist (i, j, b) :
    X = max(min( i, b.position.x+b.size.x-1 ), b.position.x)
    Y = max(min( j, b.position.y+b.size.y-1 ), b.position.y)
    return XY(X-i,Y-j)

