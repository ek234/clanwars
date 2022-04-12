import os
import time
import pickle
from components import game
import stage1, stage2, stage3
from utils import CHANGE_WEAPON
from utils import UP, RIGHT, DOWN, LEFT
from utils import SPELL_RAGE, SPELL_HEAL, SPELL_RISE
from utils import NOTSTARTED, INGAME, WON, LOST
from getinput import Get, input_to
from endpage import ending

timePerFrame = 1/game.fps
stages = [ stage1, stage2, stage3 ]
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

isKing = saveData["isKing"]

gameState = NOTSTARTED

for stageID, stage in enumerate(stages) :

    seed = saveData[stageID]["seed"]

    game.gameInit( stage.spawns, stage.townhalls_at, stage.huts_at, stage.cannons_at, stage.towers_at, stage.walls_at, seed )

    playerSpawn = saveData[stageID]["playerSpawn"]
    gameState = game.gameStart(playerSpawn, isKing)

    os.system("stty -echo")

    ite = 0
    prevFrameTime = time.time()
    while gameState is INGAME :
        ite+=1

        inp = None
        waitTime = timePerFrame - ( time.time() - prevFrameTime )
        if waitTime > 0 :
            time.sleep(waitTime)
        prevFrameTime = time.time()

        if ite in saveData[stageID]["moves"] :
            inp = saveData[stageID]["moves"][ite]

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

    ending( gameState == WON )

    if gameState != WON :
        break

    saveData[stageID]["num_ite"] = ite
