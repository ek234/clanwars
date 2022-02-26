import yaml
from utils import xy

with open("config.yaml", 'r') as data:
    config = yaml.safe_load(data)

display_size = xy( config["display"]["size"]["x"], config["display"]["size"]["y"] )
display_unit_size = xy( config["display"]["size"]["x"], config["display"]["unitsize"]["y"] )

townhall_maxhealth = config["townhall"]["maxhealth"]
townhall_size = xy( config["townhall"]["size"]["x"], config["townhall"]["size"]["y"] )

hut_maxhealth = config["hut"]["maxhealth"]
hut_size = xy( config["hut"]["size"]["x"], config["hut"]["size"]["y"] )

wall_maxhealth = config["wall"]["maxhealth"]
wall_size = xy( config["wall"]["size"]["x"], config["wall"]["size"]["y"] )

cannon_maxhealth = config["cannon"]["maxhealth"]
cannon_range = config["cannon"]["range"]
cannon_damage = config["cannon"]["damage"]
cannon_size = xy( config["cannon"]["size"]["x"], config["cannon"]["size"]["y"] )

king_speed = config["king"]["speed"]
king_damage = config["king"]["damage"]
king_maxhealth = config["king"]["maxhealth"]
king_size = xy( config["king"]["size"]["x"], config["king"]["size"]["y"] )

barbarian_speed = config["barbarian"]["speed"]
barbarian_damage = config["barbarian"]["damage"]
barbarian_maxhealth = config["barbarian"]["maxhealth"]
barbarian_size = xy( config["barbarian"]["size"]["x"], config["barbarian"]["size"]["y"] )
