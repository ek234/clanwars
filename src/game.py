from components import game
import time
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at

## TODO : avoid overlap of buildings

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )

game.gameStart(1)

game.spawn_barbarian(1)
game.spawn_barbarian(1)
game.spawn_barbarian(0)
game.spawn_barbarian(2)





