num_buildingtype = 3

# enum
UP, LEFT, DOWN, RIGHT = 'w', 'a', 's', 'd'
UP, LEFT, DOWN, RIGHT = ',', 'a', 'o', 'e'
TOWNHALL, HUT, CANNON = range(num_buildingtype)
NOTSTARTED, INGAME, WON, LOST = range(-1,3)

class xy :
    def __init__ (self, x, y) :
        self.x = x
        self.y = y

class attack_region :
    def __init__ (self, position, size) :
        self.position = position
        self.size = size

def cmp(a, b):
    return (a > b) - (a < b)

def dist (i, j, b) :
    X = max(min( i, b.position.x+b.size.x-1 ), b.position.x)
    Y = max(min( j, b.position.y+b.size.y-1 ), b.position.y)
    return xy(X-i,Y-j)

