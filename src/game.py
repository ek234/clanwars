from components import game
import time
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
import os
from utils import NOTSTARTED, INGAME, WON, LOST

## TODO : avoid overlap of buildings

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )

gameState = game.gameStart(1)

currTime = time.time()
while gameState is INGAME:
    prevTime = currTime
    currTime = time.time()
    input()
    os.system('clear')
    gameState = game.gameloop(currTime-prevTime)

os.system('clear')
print(gameState)

#game.spawn_barbarian()
#king attack
#king move
