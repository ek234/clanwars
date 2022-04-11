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
        with open("replays/"+filename, 'rb') as file :
            saveData = pickle.load( file )
    except :
        print("please enter correct filename")
    else :
        break
os.system("stty -echo")

game.gameInit( spawns, townhalls_at, huts_at, cannons_at, walls_at, saveData["seed"] )

isKing = saveData["isKing"]

gameState = game.gameStart(saveData["playerSpawn"], isKing)

ite = 0
prevFrameTime = time.time()
while gameState is INGAME :
    ite+=1

    inp = None
    waitTime = timePerFrame - ( time.time() - prevFrameTime )
    if waitTime > 0 :
        time.sleep(waitTime)
    prevFrameTime = time.time()

    if ite in saveData["moves"] :
        inp = saveData["moves"][ite]

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
        assert inp != None
        game.spawn(int(inp)-1)
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
