import os
import time
import pickle
from components import game
from initialState import spawns, townhalls_at, huts_at, cannons_at, walls_at
from utils import CHANGE_WEAPON
from utils import UP, RIGHT, DOWN, LEFT
from utils import SPELL_RAGE, SPELL_HEAL, SPELL_RISE
from utils import NOTSTARTED, INGAME, WON, LOST
from endpage import ending

timePerFrame = 1/game.fps
saveData = {}
while True :
    filename = input("enter filename: ")
    try :
        with open(filename, 'rb') as file :
            saveData = pickle.load( file )
    except :
        print("please enter correct filename")
    else :
        break
os.system("stty -echo")

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at )

gameState = game.gameStart(saveData["kingSpawn"])

ite = 0
prevFrameTime = time.time()
while gameState is INGAME :
    ite+=1

    inp = None
    waitTime = timePerFrame - ( time.time() - prevFrameTime )
    if waitTime > 0 :
        time.sleep(waitTime)
    prevFrameTime = time.time()

    if ite in saveData :
        inp = saveData[ite]

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
        assert inp != None
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

    if ite > saveData["num_ite"] :
        break

ending( gameState == WON )
