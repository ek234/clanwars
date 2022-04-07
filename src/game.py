import os
import time
import pickle
from components import game
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
from utils import CHANGE_WEAPON
from utils import UP, RIGHT, DOWN, LEFT
from utils import SPELL_RAGE, SPELL_HEAL, SPELL_RISE
from utils import NOTSTARTED, INGAME, WON, LOST
from getinput import Get, input_to
from endpage import ending

## TODO : avoid overlap of buildings

timePerFrame = 1/game.fps
seed = time.time()
filename = str(time.time())+".rpl"
saveData = {}

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at, seed )
saveData["seed"] = seed

inp = None
while inp not in { 0, 1, 2 } :
    try :
        inp = int(input("spawn king at 1, 2 or 3: ")) - 1
    except :
        inp = None
gameState = game.gameStart(inp)
saveData["kingSpawn"] = inp

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
        saveData[ite] = inp

    if inp == " " :
        if game.king != None :
            game.king.attack()
    elif inp == CHANGE_WEAPON :
        if game.king != None :
            game.king.isAxe = not game.king.isAxe
    elif inp in { UP, LEFT, DOWN, RIGHT } :
        if game.king != None :
            game.king.move(inp, timePerFrame)
    elif inp in {'1','2','3'} :
        game.spawn_barbarian(int(inp)-1)
    elif inp == SPELL_HEAL :
        game.spell_heal()
    elif inp == SPELL_RAGE :
        game.spell_rage()
    elif inp == SPELL_RISE :
        game.spell_rise()
    elif inp == '/' :
        break

    gameState = game.gameloop(timePerFrame)

saveData["num_ite"] = ite

ending( gameState == WON )

print("saving data in", filename)
os.system("mkdir -p replays")
with open("replays/"+filename, 'wb') as file :
    pickle.dump( saveData, file )
