"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import random
from ModelFish import FishCreature
from ModelSphere import SphereCreature


from Point import Point
from Component import Component
from Animation import Animation
from ModelTank import Tank
from ModelLinkage import Linkage
from EnvironmentObject import EnvironmentObject
from ModelRobot import RobotCreature
from TriPrismComponent import TriPrismComponent


class Vivarium(Component, Animation):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None
    obj_id = -1

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent):
        self.parent = parent

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(parent, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))
        
  

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]

        
        f1=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.07, 0.03, -0.01],scale=0.5, isPrey=True)
        f2=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.03, 0.04, -0.04] ,scale=0.5, isPrey=True)
        f3=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.07, 0.03, -0.01],scale=0.5, isPrey=True)
        f4=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.03, 0.04, -0.04] ,scale=0.5, isPrey=True)
        f5=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.07, 0.03, -0.01],scale=0.5, isPrey=True)
        f6=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.03, 0.04, -0.04] ,scale=0.5, isPrey=True)
        f_predator=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.01, 0.02, 0.01], scale=0.5, isPrey=False)
        f_predator_2=FishCreature(parent, pos=Point((0, 0, 0)), init_vel=[0.01, 0.02, 0.01], scale=0.5, isPrey=False)

        # bug - when position is set in the constructor of the creatures, the bounding box of the 
        # vivarium is shifted and all of the collision detection code breaks
        f1.setCurrentPosition(Point((1, 0, 0)))
        f2.setCurrentPosition(Point((1, 0, 0)))
        f3.setCurrentPosition(Point((1, 0, 0)))
        f4.setCurrentPosition(Point((1, 0, 0)))
        f5.setCurrentPosition(Point((1, 0, 0)))
        f6.setCurrentPosition(Point((1, 0, 0)))
        f_predator.setCurrentPosition(Point((1, 1, 0)))
        f_predator_2.setCurrentPosition(Point((1, 1, 0)))

        self.addNewObjInTank(f1)
        self.addNewObjInTank(f2)
        self.addNewObjInTank(f3)
        self.addNewObjInTank(f4)
        self.addNewObjInTank(f5)
        self.addNewObjInTank(f6)
        self.addNewObjInTank(f_predator)
        self.addNewObjInTank(f_predator_2)

        robot = RobotCreature(parent, Point((0, 0, 0)), init_vel=[-0.04, 0.0, 0.0])
        robot.setDefaultAngle(robot.vAxis, 90)
        robot.setCurrentPosition(Point((0, 0, 1)))
        self.addNewObjInTank(robot)
        
    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """
        for c in self.components[::-1]:
            if isinstance(c, Animation):
                c.animationUpdate()
        
        for idx, c in enumerate(self.components[1:]):
            x, y, z = c.current_position.coords
            potential = c.addPotentials()
            x += c.velocity[0] + potential[0]
            y += c.velocity[1] + potential[1]
            z += c.velocity[2] + potential[2]
            print(x)
            c.setCurrentPosition(Point((x, y, z)))
            c.bound_center = (Point((x, y, z)))
            collided_obj = c.collision_detection()
            if (collided_obj != [] and collided_obj is not None):
                for obj in collided_obj:
                    self.delObjInTank(obj)
                self.update()
    

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components
