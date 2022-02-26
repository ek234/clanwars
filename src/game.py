from components import game
import time
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
import os
from utils import NOTSTARTED, INGAME, WON, LOST
from input import Get, input_to

## TODO : avoid overlap of buildings

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )

gameState = game.gameStart(1)

prevTime = currTime = time.time()
while gameState is INGAME:
    prevTime = currTime
    currTime = time.time()
    dt = currTime - prevTime
    inp = input_to(Get())
    if inp == " " :
        if game.king != None :
            game.king.attack()
    elif inp in {'w','a','s','d'} :
        if game.king != None :
            game.king.move(inp, dt)
    elif inp in {'1','2','3'} :
        game.spawn_barbarian(int(inp)-1)
    sleepTime = 1./game.fps - dt
    if sleepTime > 0 :
        time.sleep(sleepTime)
    os.system('clear')
    gameState = game.gameloop(dt)

print(gameState)

#game.spawn_barbarian()
#king attack
#king move
