num_buildingtype = 3

# enum
UP, LEFT, DOWN, RIGHT = 'w', 'a', 's', 'd'
TOWNHALL, HUT, CANNON = range(num_buildingtype)
NOTSTARTED, INGAME, WON, LOST = range(-1,3)

class xy :
    def __init__ (self, x, y) :
        self.x = x
        self.y = y

def dist (i, j, b) :
    ## normally these is the correct formulae:
    #X = max(min( i, b.position.x+b.size.x-1 ), b.position.x)
    #Y = max(min( j, b.position.y+b.size.y-1 ), b.position.y)
    ## but, we want to avoid collision
    ## so, we stop the troops 1 block away from the buildings
    X = max(min( i, b.position.x+b.size.x ), b.position.x-1)
    Y = max(min( j, b.position.y+b.size.y ), b.position.y-1)
    return xy(X-i,Y-j)

