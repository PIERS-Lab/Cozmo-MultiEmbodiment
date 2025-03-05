#this driver will test the custom functionality made  for the trust and teamwork project
from cozCube import coz
import cozmo
from cozmo import *

import asyncio
async def test_find(connection):
    print("testing cube recognition")
    print ("Please input cube ID to assign the cozmo to: ")
    testiee = coz(await connection.wait_for_robot(), input())
    print ("please input the cube Id that cozmo should grab: ")
    result =await testiee.findCube(input())
    if (result):
        testiee.system.say_text("Cube Found!", play_excited_animation=True,use_cozmo_voice=True).wait_for_completed()
    #print("i'm out!\n")
    return 

async def test_move(connection):
    print("Testing cube relocation")
    print ("Please input cube ID to assign the cozmo to: ")
    ID = input()
    testiee = coz(await connection.wait_for_robot(), ID)
    await testiee.moveCube(ID)



cozmo.connect_with_tkviewer(test_move)
