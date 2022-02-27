#import yaml
from utils import xy

#with open("initialState.yaml", 'r') as data:
    #state = yaml.safe_load(data)

spawns = [
    xy(1,1),
    xy(1,20),
    xy(20,1)
]

townhalls_at = [
    xy(60,13)
]

huts_at = [
    xy(41,1),
    xy(21,20),
    xy(23,1),
    xy(23,4),
    xy(23,7),
]

cannons_at = [
    xy(3,3),
    xy(12,1)
]

walls_at = [
    xy(3,7),
    xy(3,8),
    xy(3,9),
    xy(3,10),
    xy(2,10),
    xy(1,10),
    xy(1,11)
]
