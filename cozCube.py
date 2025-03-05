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
        await self.system.say_text("I can't do that! " + detail).wait_for_completed()

    #It needs to take input as apart of analyzing the task
    #returns the found lightcube object
    async def findCube(self, cbID):
        await self.system.set_head_angle(degrees(0)).wait_for_completed()
        if (cbID != self.cubeID):
            await self.failmsg(detail = "as I don't own this cube")
            return
        #look for cube
        
        #this line is causing some bad mojo jojo 
       
        currBehavior = self.system.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try: 
            found = await self.system.world.wait_for_observed_light_cube(timeout = 20)
            #print(found.cube_id)
            while (int(found.cube_id) != int(cbID)):
                #print("Found has ID: ", found.cube_id, "\n", "cbID: ", cbID)
                found = await self.system.world.wait_for_observed_light_cube(timeout = 10, include_existing=False)
                #if we can't find the right cube, fail
            #print("exited loop!\n")
        except asyncio.TimeoutError:
            cozmo.behavior.Behavior.stop(currBehavior)
            await self.system.say_text("I couldn't find my cube", use_cozmo_voice=True).wait_for_completed()
            
            #print("returning!\n")
            return False
        #print("starting Cube Recognition process\n")    
        cozmo.behavior.Behavior.stop(currBehavior)
        #await self.system.say_text("Cube Found!", play_excited_animation=True,use_cozmo_voice=True).wait_for_completed()
        
        
        return found
    #end point will be a cozmo pose
    # if return _to_start is set to true
    # cozmo will Ignore the end point argument and just return to his starting position if not given one
    async def moveCube(self, cbID, endpoint = cozmo.util.Pose(0,0, 0, angle_z=cozmo.util.degrees(0))):
        temp = await self.findCube(cbID)
        if (temp == False):
            return False
        #cozmo.robot.Robot.dock_with_cube(self,temp, None, cozmo.robot_alignment.RobotAlignmentTypes.LiftPlate, None, False, 3)
        #cozmo.robot.Robot.set_lift_height(self, 1.0)
        #cozmo.robot.Robot.go_to_pose(endpoint)
        # cozmo.robot.Robot.set_lift_height( 0.0)
        # cozmo.robot.Robot.drive_straight(-5, 1)
        await self.system.dock_with_cube(temp, None, cozmo.robot_alignment.RobotAlignmentTypes.LiftPlate, None, False, 3).wait_for_completed()
        await self.system.set_lift_height(1.0).wait_for_completed()
        await self.system.go_to_pose(endpoint).wait_for_completed()
        await self.system.set_lift_height(0).wait_for_completed()
        #back away from cube to avoid messing with the cube
        await self.system.drive_straight(cozmo.util.distance_inches(-1), cozmo.util.speed_mmps(100)).wait_for_completed()
    #Recongizing a certain position/destination
    #   color detection?
    #   Work on recognition of unique objects
    #