'''This class serves both as an easy way to run multiple robots, and
as the vehichle to implement the game, all needed functions and behaviors will be defined here'''
import asyncio 
import time
import cozmo 
from cozmo import *
from cozmo.util import degrees
from cozmo.objects import CustomObjectMarkers
class coz:

    def __init__ (self, system, cube_Num):
        # robot is a cozmo.conn.cozmoConnection.robot.Robot object
        self.robot = system
        self.cubeID = cube_Num
        # from the person's position, goal 0 is far left, goal 1 is middle, goal 2 is far right
        self.goals = None
    async def create(system, cube_num):
        self = coz(system, cube_num)
        self.goals = [await self.robot.world.define_custom_wall(cozmo.objects.CustomObjectTypes.CustomType02,
                                              CustomObjectMarkers.Triangles5,
                                              150, 120,
                                              132, 132, True)]
        # set up goal markers Goals are x by x by x (still wip) at their base, a wall is used due to other options being not suitable
        return self
        
    async def failmsg(self, detail = "."):
        await self.robot.say_text("I can't do that! " + detail).wait_for_completed()

    # It needs to take input as apart of analyzing the task
    # returns the found lightcube object
    async def findCube(self, cbID):
        await self.robot.set_head_angle(degrees(0)).wait_for_completed()
        if (cbID != self.cubeID):
            await self.failmsg(detail = "as I don't own this cube")
            return
        # look for cube
        ''' To-Do: make this more robust, 
        have cozmo search a little harder (maybe have him move around to account for the poor range of his vision)'''
        currBehavior = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        try: 
            found = await self.robot.world.wait_for_observed_light_cube(timeout = 20)
            while (int(found.cube_id) != int(cbID)):
                found = await self.robot.world.wait_for_observed_light_cube(timeout = 10, include_existing=False)
                # if we can't find the right cube, fail
        except asyncio.TimeoutError:
            cozmo.behavior.Behavior.stop(currBehavior)
            await self.robot.say_text("I couldn't find my cube", use_cozmo_voice=True).wait_for_completed()
            return False
        cozmo.behavior.Behavior.stop(currBehavior)
        
        
        return found
    async def lift_cube(self, target):
        await self.robot.dock_with_cube(target, num_retries=3, approach_angle=cozmo.util.degrees(0)).wait_for_completed()
        await self.robot.set_lift_height(1.0).wait_for_completed()

    async def drop_cube(self):
        await self.robot.set_lift_height(0).wait_for_completed()
        # back away from cube to avoid messing with it accidentally
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
            return False 
        print("goal found!") 
        cozmo.behavior.Behavior.stop(currBehavior)
        print (found.obj.pose)
        return found.obj
    
    async def deliver(self, goal):
        ''' Note that due to the restrictions of the SDK, cozmo will be seeing
        the goals as a wall, so an offset must be applied so cozmo arrives at the correct location
        Also: this current offset will not be finalized until a goal design is complete '''
        # this must be done like this, the API does not like existing poses being edited for some reason
        dest = cozmo.util.Pose(goal.pose._position.x - 144, goal.pose._position.y, goal.pose.position.z, 
                               angle_z=goal.pose._rotation.angle_z, origin_id=goal.pose._origin_id )
        await self.robot.go_to_pose(dest).wait_for_completed()
        await self.drop_cube()


        
    # end point is a cozmo pose
    '''  if return _to_start is set to true cozmo will Ignore the end point argument 
    and just return to his starting position if not given one '''
    async def moveCube(self, cbID, endpoint = cozmo.util.Pose(0,0, 0, angle_z=cozmo.util.degrees(0))):
        temp = await self.findCube(cbID)
        if (temp == False):
            return False
        await self.lift_cube(temp)
        await self.robot.go_to_pose(endpoint).wait_for_completed()
        await self.drop_cube()