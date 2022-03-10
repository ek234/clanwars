import os
import time
from components import game
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
from utils import UP, RIGHT, DOWN, LEFT
from utils import SPELL_RAGE, SPELL_HEAL
from utils import NOTSTARTED, INGAME, WON, LOST
from getinput import Get, input_to

## TODO : avoid overlap of buildings

timePerFrame = 1/game.fps
os.system("stty -echo")

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )
gameState = game.gameStart(1)

ite = 0
frame_time_end = time.time()
while gameState is INGAME :
    frame_time_start = time.time()

    ite+=1

    inp = None
    while True :
        waitTime = timePerFrame - ( time.time() - frame_time_end )
        if waitTime < 0 :
            break
        if inp == None :
            inp = input_to(Get(), waitTime)
    frame_time_end = time.time()

    if inp == " " :
        if game.king != None :
            game.king.attack()
    elif inp in { UP, LEFT, DOWN, RIGHT } :
        if game.king != None :
            game.king.move(inp, timePerFrame)
    elif inp in {'1','2','3'} :
        game.spawn_barbarian(int(inp)-1)
    elif inp == SPELL_HEAL :
        game.spell_heal()
    elif inp == SPELL_RAGE :
        game.spell_rage()
    elif inp == '/' :
        break

    gameState = game.gameloop(ite, timePerFrame)

if gameState == WON :
    print("you win")
elif gameState == LOST :
    print("better luck next time")
