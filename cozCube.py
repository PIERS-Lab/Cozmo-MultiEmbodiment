#this class enables wuick initialization of cozmo robots and assigns them a cube, 
#aswell as handling reconition of if a given task is possible (in relation to the cubes)
import asyncio 
import time
import cozmo 
from cozmo import *
from cozmo.util import degrees

#this is like the active connection, so most actions the cozmo will take are used through this object
#cozmo.conn.robot.Robot.
#cozmo.robot.Robot.

class coz:

    def __init__ (self, system, cube_Num):
        #system will  be a cozmo.conn.cozmoConnection.robot.Robot object
        self.system = system
        self.cubeID = cube_Num
        print("constructor called!\n")

    async def failmsg(self, detail = "."):
        #self.system.robot.Robot.say_text("My apolgies, But I am unable to fufill your request " + detail, use_cozmo_voice=True)
        await self.system.say_text("My apologies, But I am unable to fufill your request " + detail).wait_for_completed()

    #It needs to take input as apart of analyzing the task
    async def findCube(self, cbID):
        await self.system.set_head_angle(degrees(0)).wait_for_completed()
        if (cbID != self.cubeID):
            await self.failmsg(detail = "as I cannot move this cube")
            return
        #look for cube
        currBehavior = self.system.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try: 
            found = await self.system.world.wait_for_observed_light_cube(timeout = 40)
            print(found.cube_id)
            while (int(found.cube_id) != int(cbID)):
                #print("Found has ID: ", found.cube_id, "\n", "cbID: ", cbID)
                found = await self.system.world.wait_for_observed_light_cube(timeout = 10, include_existing=False)
                #if we can't find the right cube, fail
            print("exited loop!\n")
        except asyncio.TimeoutError:
            cozmo.behavior.Behavior.stop(currBehavior)
            await self.system.say_text("I couldn't find my cube", use_cozmo_voice=True).wait_for_completed()
            
            print("returning!\n")
            return False
        print("strting Cube Reconition process\n")    
        cozmo.behavior.Behavior.stop(currBehavior)
        await self.system.say_text("Cube Found!", play_excited_animation=True,use_cozmo_voice=True).wait_for_completed()
        #Cozmo has some sort of way to align with the cube, figure this out and use it
        #try just picking up the cube and moving it to it's start for now, command processing is still a ways away.....
        
        return True

   