from components import game
import time
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
from utils import UP, RIGHT, DOWN, LEFT
from utils import NOTSTARTED, INGAME, WON, LOST
from getinput import Get, input_to

## TODO : avoid overlap of buildings

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )

gameState = game.gameStart(1)

if gameState == NOTSTARTED :
    time.sleep(0.1)
currTime = time.time()
while gameState is INGAME :

    prevTime = currTime
    currTime = time.time()
    dt = currTime - prevTime
    waitTime = max(1./game.fps - dt, 0.1)

    inp = input_to(Get(), waitTime)
    if inp == " " :
        if game.king != None :
            game.king.attack()
    elif inp in { UP, LEFT, DOWN, RIGHT } :
        if game.king != None :
            game.king.move(inp, dt)
    elif inp in {'1','2','3'} :
        game.spawn_barbarian(int(inp)-1)
    elif inp == 'q' :
        break

    currTime = time.time()
    dt = currTime - prevTime
    waitTime = 1./game.fps - dt
    if waitTime > 0 :
        time.sleep(waitTime)

    gameState = game.gameloop(dt)

if gameState == WON :
    print("you win")
elif gameState == LOST :
    print("better luck next time")

#game.spawn_barbarian()
#king attack
#king move
