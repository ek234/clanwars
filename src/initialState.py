#import yaml
from utils import XY

#with open("initialState.yaml", 'r') as data:
    #state = yaml.safe_load(data)

spawns = [
    XY(1,1),
    XY(1,20),
    XY(20,1)
]

townhalls_at = [
    XY(60,13)
]

huts_at = [
    XY(41,1),
    XY(21,20),
    XY(23,1),
    XY(23,4),
    XY(23,7),
]

cannons_at = [
    XY(3,3),
    XY(12,1)
]

walls_at = [
    XY(3,7),
    XY(3,8),
    XY(3,9),
    XY(3,10),
    XY(2,10),
    XY(1,10),
    XY(1,11)
]
