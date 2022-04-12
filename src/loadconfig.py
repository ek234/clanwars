import yaml
from utils import XY

with open("config.yaml", 'r') as data:
    config = yaml.safe_load(data)

display_size = XY( config["display"]["size"]["x"], config["display"]["size"]["y"] )
display_unit_size = XY( config["display"]["unitsize"]["x"], config["display"]["unitsize"]["y"] )
display_fps = config["display"]["fps"]

townhall_maxhealth = config["townhall"]["maxhealth"]
townhall_size = XY( config["townhall"]["size"]["x"], config["townhall"]["size"]["y"] )

hut_maxhealth = config["hut"]["maxhealth"]
hut_size = XY( config["hut"]["size"]["x"], config["hut"]["size"]["y"] )

wall_maxhealth = config["wall"]["maxhealth"]
wall_size = XY( config["wall"]["size"]["x"], config["wall"]["size"]["y"] )

cannon_maxhealth = config["cannon"]["maxhealth"]
cannon_range = config["cannon"]["range"]
cannon_damage = config["cannon"]["damage"]
cannon_size = XY( config["cannon"]["size"]["x"], config["cannon"]["size"]["y"] )

tower_maxhealth = config["tower"]["maxhealth"]
tower_range = config["tower"]["range"]
tower_radius = config["tower"]["radius"]
tower_damage = config["tower"]["damage"]
tower_size = XY( config["tower"]["size"]["x"], config["tower"]["size"]["y"] )

king_speed = config["king"]["speed"]
king_damage = config["king"]["damage"]
king_maxhealth = config["king"]["maxhealth"]
king_axeRange = config["king"]["range"]
king_size = XY( config["king"]["size"]["x"], config["king"]["size"]["y"] )

queen_speed = config["queen"]["speed"]
queen_damage = config["queen"]["damage"]
queen_maxhealth = config["queen"]["maxhealth"]
queen_range = config["queen"]["range"]
queen_radius = config["queen"]["radius"]
queen_erange = config["queen"]["erange"]
queen_eradius = config["queen"]["eradius"]
queen_size = XY( config["queen"]["size"]["x"], config["queen"]["size"]["y"] )

barbarian_speed = config["barbarian"]["speed"]
barbarian_damage = config["barbarian"]["damage"]
barbarian_maxhealth = config["barbarian"]["maxhealth"]
barbarian_size = XY( config["barbarian"]["size"]["x"], config["barbarian"]["size"]["y"] )
barbarian_maxnum = config["barbarian"]["maxnum"]

archer_speed = config["archer"]["speed"]
archer_damage = config["archer"]["damage"]
archer_maxhealth = config["archer"]["maxhealth"]
archer_range = config["archer"]["range"]
archer_size = XY( config["archer"]["size"]["x"], config["archer"]["size"]["y"] )
archer_maxnum = config["archer"]["maxnum"]

ballon_speed = config["ballon"]["speed"]
ballon_damage = config["ballon"]["damage"]
ballon_maxhealth = config["ballon"]["maxhealth"]
ballon_size = XY( config["ballon"]["size"]["x"], config["ballon"]["size"]["y"] )
ballon_maxnum = config["ballon"]["maxnum"]

rage_timecap = config["spell"]["rage"]["timecap"]
