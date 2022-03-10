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

king_speed = config["king"]["speed"]
king_damage = config["king"]["damage"]
king_maxhealth = config["king"]["maxhealth"]
king_axeRange = config["king"]["axeRange"]
king_size = XY( config["king"]["size"]["x"], config["king"]["size"]["y"] )

barbarian_speed = config["barbarian"]["speed"]
barbarian_damage = config["barbarian"]["damage"]
barbarian_maxhealth = config["barbarian"]["maxhealth"]
barbarian_size = XY( config["barbarian"]["size"]["x"], config["barbarian"]["size"]["y"] )

rage_timecap = config["spell"]["rage"]["timecap"]
