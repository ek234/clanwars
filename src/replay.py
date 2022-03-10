import os
import time
import pickle
from components import game
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
from utils import UP, RIGHT, DOWN, LEFT
from utils import SPELL_RAGE, SPELL_HEAL
from utils import NOTSTARTED, INGAME, WON, LOST

## TODO : avoid overlap of buildings

timePerFrame = 1/game.fps
filename = input("enter filename: ")
movelist = {}
with open(filename, 'rb') as file :
    movelist = pickle.load( file )
os.system("stty -echo")

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )
gameState = game.gameStart(1)

ite = 0
prevFrameTime = time.time()
while gameState is INGAME :
    ite+=1

    inp = None
    waitTime = timePerFrame - ( time.time() - prevFrameTime )
    if waitTime > 0 :
        time.sleep(waitTime)
    prevFrameTime = time.time()

    if ite in movelist :
        inp = movelist[ite]

    if inp == " " :
        if game.king != None :
            game.king.attack()
    elif inp in { UP, LEFT, DOWN, RIGHT } :
        if game.king != None :
            game.king.move(inp, timePerFrame)
    elif inp in {'1','2','3'} :
        assert inp != None
        game.spawn_barbarian(int(inp)-1)
    elif inp == SPELL_HEAL :
        game.spell_heal()
    elif inp == SPELL_RAGE :
        game.spell_rage()
    elif inp == '/' :
        break

    gameState = game.gameloop(timePerFrame)

if gameState == WON :
    print("you win")
elif gameState == LOST :
    print("better luck next time")
