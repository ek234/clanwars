import os
import time
import pickle
from components import game
from stage1 import spawns, townhalls_at, huts_at, cannons_at, towers_at, walls_at
from utils import CHANGE_WEAPON
from utils import UP, RIGHT, DOWN, LEFT
from utils import SPELL_RAGE, SPELL_HEAL, SPELL_RISE
from utils import NOTSTARTED, INGAME, WON, LOST
from getinput import Get, input_to
from endpage import ending

## todo : avoid overlap of buildings

# TODO : add readme

timePerFrame = 1/game.fps
seed = time.time()
filename = str(time.time())+".rpl"
saveData = {}
saveData["moves"] = {}

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, towers_at, walls_at, seed )
saveData["seed"] = seed

isKing = None
while isKing not in { "k", "q" } :
    isKing = input("press k for king and q for queen : ")
isKing = isKing == "k"
saveData["isKing"] = isKing
inp = None
while inp not in { 0, 1, 2 } :
    try :
        inp = int(input("spawn player at 1, 2 or 3: ")) - 1
    except :
        inp = None
gameState = game.gameStart(inp, isKing)
saveData["playerSpawn"] = inp

os.system("stty -echo")

ite = 0
prevFrameTime = time.time()
while gameState is INGAME :
    ite+=1

    inp = None
    waitTime = timePerFrame - ( time.time() - prevFrameTime )
    if waitTime > 0 :
        inp = input_to(Get(), waitTime)
    waitTime = timePerFrame - ( time.time() - prevFrameTime )
    if waitTime > 0 :
        time.sleep(waitTime)
    prevFrameTime = time.time()

    if inp != None :
        saveData["moves"][ite] = inp

    if inp == " " :
        if game.player != None :
            game.player.attack()
    elif inp == CHANGE_WEAPON :
        if game.player != None :
            game.player.switchWeapon()
    elif inp in { UP, LEFT, DOWN, RIGHT } :
        if game.player != None :
            game.player.move(inp, timePerFrame)
    elif inp in {'1','2','3', '4', '5', '6', '7', '8', '9'} :
        game.spawn(int(inp)-1)
    elif inp == SPELL_HEAL :
        game.spell_heal()
    elif inp == SPELL_RAGE :
        game.spell_rage()
    elif inp == SPELL_RISE :
        game.spell_rise()
    elif inp == '/' :
        break

    gameState = game.gameloop(timePerFrame, ite)

saveData["num_ite"] = ite

ending( gameState == WON )

print("saving data in", filename)
os.system("mkdir -p replays")
with open("replays/"+filename, 'wb') as file :
    pickle.dump( saveData, file )
