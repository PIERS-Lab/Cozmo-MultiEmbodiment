#this class enables wuick initialization of cozmo robots and assigns them a cube, 
#aswell as handling reconition of if a given task is possible (in relation to the cubes)
import asyncio 
import time
import cozmo 
from cozmo import *
from cozmo.util import degrees
from cozmo.objects import CustomObjectMarkers

#this is like the active connection, so most actions the cozmo will take are used through this object
#cozmo.conn.robot.Robot.
#cozmo.robot.Robot.

class coz:

    def __init__ (self, system, cube_Num):
        #system will be a cozmo.conn.cozmoConnection.robot.Robot object
        self.robot = system
        self.cubeID = cube_Num
        #from the person's position, goal 0 is far left, goal 1 is middle, goal 2 is far right
        self.goals = None
        self.cozmoDispatcher = cozmo.event.Dispatcher(loop=asyncio.get_event_loop())
        
    async def create(system, cube_num):
        self = coz(system, cube_num)
        self.goals = [await self.robot.world.define_custom_wall(cozmo.objects.CustomObjectTypes.CustomType02,
                                              CustomObjectMarkers.Triangles5,
                                              150, 120,
                                              50, 30, True)]
        # set up goal markers Goals are x by x by x at their base, a wall is used due to other options being not suitable
        return self
        
    async def failmsg(self, detail = "."):
        #self.system.robot.Robot.say_text("My apolgies, But I am unable to fufill your request " + detail, use_cozmo_voice=True)
        await self.robot.say_text("I can't do that! " + detail).wait_for_completed()

    #It needs to take input as apart of analyzing the task
    #returns the found lightcube object
    async def findCube(self, cbID):
        await self.robot.set_head_angle(degrees(0)).wait_for_completed()
        if (cbID != self.cubeID):
            await self.failmsg(detail = "as I don't own this cube")
            return
        #look for cube
        #To-Do: make this more robust, 
        #have cozmo search a little harder (maybe have him move around to account for the poor range of his vision)
        currBehavior = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try: 
            found = await self.robot.world.wait_for_observed_light_cube(timeout = 20)
            #print(found.cube_id)
            while (int(found.cube_id) != int(cbID)):
                #print("Found has ID: ", found.cube_id, "\n", "cbID: ", cbID)
                found = await self.robot.world.wait_for_observed_light_cube(timeout = 10, include_existing=False)
                #if we can't find the right cube, fail
            #print("exited loop!\n")
        except asyncio.TimeoutError:
            cozmo.behavior.Behavior.stop(currBehavior)
            await self.robot.say_text("I couldn't find my cube", use_cozmo_voice=True).wait_for_completed()
            
            #print("returning!\n")
            return False
        #print("starting Cube Recognition process\n")    
        cozmo.behavior.Behavior.stop(currBehavior)
        #await self.system.say_text("Cube Found!", play_excited_animation=True,use_cozmo_voice=True).wait_for_completed()
        
        
        return found
    async def lift_cube(self, target):
        await self.robot.dock_with_cube(target, num_retries=3, approach_angle=cozmo.util.degrees(0)).wait_for_completed()
        await self.robot.set_lift_height(1.0).wait_for_completed()

    async def drop_cube(self):
        await self.robot.set_lift_height(0)
        #back away from cube to avoid messing with it accidentally
        await self.robot.drive_straight(cozmo.util.distance_inches(-1), cozmo.util.speed_mmps(100)).wait_for_completed()
    # if cozmo fails for any reason, false is returned, other wise the pose of the desired object is returned instead
    async def find_goal(self, goalNum):
        await self.robot.set_head_angle(degrees(0)).wait_for_completed()
        if goalNum < 0 or goalNum > 2:
            self.failmsg("as that goal is not real!")
            return False 
        
        # look for goal
        # To-Do: make this more robust, 
        # have cozmo search a little harder (maybe have him move around to account for the poor range of his vision)
        try:
            # check if we found the correct goals
            currBehavior = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            found = await self.robot.wait_for(cozmo.objects.EvtObjectObserved,  timeout = 40)
            while (isinstance(found.obj, cozmo.objects.LightCube) or self.goals[goalNum].object_type != found.obj.object_type):
                found = await self.robot.wait_for(cozmo.objects.EvtObjectObserved,  timeout = 40)
                
        except asyncio.TimeoutError:
            cozmo.behavior.Behavior.stop(currBehavior)
            await self.robot.say_text("I couldn't find the goal", use_cozmo_voice=True).wait_for_completed()
            # print("returning!\n")
            return False
        # print("starting Cube Recognition process\n") 
        print("goal found!") 
        cozmo.behavior.Behavior.stop(currBehavior)
        print (found.obj.pose)
        return found.obj
        # await self.system.say_text("Cube Found!", play_excited_animation=True,use_cozmo_voice=True).wait_for_completed()

    async def deliver(self, goal):
        # note that due to the restrictions of the SDK, cozmo will be seeing
        # the goals as a wall, so an offset must be applied so cozmo arrives at the correct location
        print(goal)
        self.robot.go_to_object(self.robot, goal, cozmo.util.distance_mm(90))
        self.drop_cube()


        
    # end point is a cozmo pose
    # if return _to_start is set to true
    # cozmo will Ignore the end point argument and just return to his starting position if not given one
    async def moveCube(self, cbID, endpoint = cozmo.util.Pose(0,0, 0, angle_z=cozmo.util.degrees(0))):
        temp = await self.findCube(cbID)
        if (temp == False):
            return False
        await self.lift_cube(temp)
        await self.robot.go_to_pose(endpoint).wait_for_completed()
        await self.drop_cube()
    # Takes in an object observed event, and verifies that it is the correct goal to go to
    # use custom objects to reconize custom goal, will likely have to do something wierd to work with restrictions