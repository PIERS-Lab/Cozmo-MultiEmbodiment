from coz import coz
import cozmo
from cozmo import * 
import asyncio
#note: implement differant control paths to determine how many connections are to be made
async def test(connection):
    print ("Please input cube ID to assign the cozmo to: ")
    testiee = coz(await connection.wait_for_robot(), input())
    print ("please input the cube Id that cozmo should grab: ")
    await testiee.grabCube(input())

cozmo.connect_with_tkviewer(test)

