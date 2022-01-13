"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import random

from Point import Point
from Component import Component
from Animation import Animation
from EnvironmentObject import EnvironmentObject
from RobotArmComponent import ArmComponent
from LegComponent import LegComponent
from BodyComponent import BodyComponent
from TailComponent import TailComponent
import math
import numpy as np

class RobotCreature(Component, Animation, EnvironmentObject):
    radius = None
    components = []
    scale = None

    def __init__(self, parent, pos, scale=[1, 1, 1], init_vel = [0.01, 0.01, 0.01]):
        super(RobotCreature, self).__init__(pos)

        position = pos
        self.species_id = 3
        self.obj_id = hash(self)
        self.scale = scale
        self.velocity = [0.01, 0.01, 0.01]
        self.bound_center = position
        self.bound_radius = 0.7
        
        startpt = Point((0, 0.5, 0))
        arm_startpt = Point((0, 0.6, 0))
        rightleg_startpt = Point((0, 0.5, -0.2))
        leftleg_startpt = Point((0, 0.5, 0.2))
        #self.global_components.append(ModelAxes(self, Point((-1, -1, -1)))) # coordinate system with x, y, z axes
        #m2 = ModelLinkage(self, Point((0, 0, 0)))  # our model linkage (give it handle to parent object and attach it to objact i think)
       # global_components.append(SphereComponent(self, Point((0, 0.2, 0))))
        #m4 = CylinderComponent(self, Point((0, 1, 0)))
        body = BodyComponent(parent, startpt)
        right_leg = LegComponent(parent, rightleg_startpt, rightLeg=True)
        left_leg = LegComponent(parent, leftleg_startpt)
        right_arm = ArmComponent(parent, arm_startpt, rightArm=True)
        left_arm = ArmComponent(parent, arm_startpt)
        tail = TailComponent(parent, startpt)
        self.components.append(body)
        self.components.append(right_arm)
        self.components.append(left_arm)
        self.components.append(right_leg)
        self.components.append(left_leg)
        self.components.append(tail)
        for c in self.components:
            self.addChild(c)
        self.components = []
        self.animatedComponents = [right_arm, left_arm]
       
        

    def animationUpdate(self):
        for c in self.animatedComponents:
           c.animationUpdate()
        self.update()
        
    def calcRotationMatrix(self):
        '''
            Currently broken, but this function calculates the rotation matrix needed to reorient 
            a creature in the case of coliision with another env_obj

            Calculates a new basis given the velocity vector of the object, and then rotates the figure such that it is facing the right direction 
        '''
        pass
        up_vector = np.array([0, 1, 0])
        unit_velocity = self.velocity/np.linalg.norm(self.velocity)
        sub_vector_1 = np.cross(unit_velocity, up_vector)
        sub_vector_2 = np.cross(sub_vector_1, up_vector)
        unit_velocity = np.append(unit_velocity, [0])
        sub_vector_1 = np.append(sub_vector_1, [0])
        sub_vector_2 = np.append(sub_vector_2, [0])
        w = np.array([0, 0, 0, 1])
        r = np.array([unit_velocity, sub_vector_1, sub_vector_2, w])
        self.setPreRotation(r.T)

    def addPotentials(self):
        '''
        calculates the gradient of the total potentail function of the object
        (Assumes that every creature has a spherical potential, but other potentials would be an easy check)
        '''
        pos_vec = self.current_position.getCoords()
        gradient = [0, 0, 0]
        pass
        for env in self.env_obj_list[1:]:
            pass
            if isinstance(env, Component) and self.obj_id != env.obj_id: 
                env_pos_vec = env.current_position.getCoords()
                if (env.species_id > self.species_id):
                    gradient[0] += pos_vec[0] - env_pos_vec[0]
                    gradient[1] += pos_vec[1] - env_pos_vec[1]
                    print(gradient[1])
                    gradient[2] += pos_vec[2] - env_pos_vec[2]

                elif (env.species_id < self.species_id):
                    gradient[0] += env_pos_vec[0] - pos_vec[0]
                    gradient[1] += env_pos_vec[1] - pos_vec[1]
                    gradient[2] += env_pos_vec[2] - pos_vec[2]

        gradient[0] *= 2
        gradient[1] *= 2
        gradient[2] *= 2

        norm = math.sqrt(gradient[0]**2 + gradient[1]**2 + gradient[2]**2)
        norm=1250 #the original gradient was too large and blew the objects out of view, so a scale was needed
        gradient = [gradient[0]/norm, gradient[1]/norm, gradient[2]/norm]
        #print(gradient)
        return gradient

    def collision_detection(self):
        '''
        Simple collision detection with the wall and other objects. If the current object is a predator object,
        it logs all of the pray objects into a list and outputs the list for the vivarium to remove.
        '''
        #self.calcRotationMatrix()
        collided_objects = []
        def distance(center_a: Point, center_b: Point):
            x1, y1, z1 = center_a.getCoords()
            x2, y2, z2 = center_b.getCoords()
            x_delta = (x2-x1)**2
            y_delta = (y2-y1)**2
            z_delta = (z2-z1)**2
            return math.sqrt(x_delta + y_delta + z_delta)

        x = self.bound_center.coords[0]
        y = self.bound_center.coords[1]
        z = self.bound_center.coords[2]

        x_min = x - self.bound_radius
        x_max = x + self.bound_radius

        y_min = y - self.bound_radius
        y_max = y + self.bound_radius

        z_min = z - self.bound_radius
        z_max = z + self.bound_radius
        #print(x_min, y_min, z_min)

        if (x_min <= -2.0 or x_max >= 2.0):
            #self.setPreRotation(self.calcRotationMatrix())
            self.velocity[0] = - self.velocity[0]
            if self.velocity[1] == 0.0:
                self.velocity[1] = 0.01
            if self.velocity[2] == 0.0:
                self.velocity[2] == 0.01
        if (y_min <= -2.0 or y_max >= 2.0):
            #self.setPreRotation(self.calcRotationMatrix())
            self.velocity[1] = - self.velocity[1]
            if self.velocity[0] == 0.0:
                self.velocity[0] = 0.01
            if self.velocity[2] == 0.0:
                self.velocity[2] == 0.01
        if (z_min <= -2.0 or z_max >= 2.0):
            #self.setPreRotation(self.calcRotationMatrix())
            self.velocity[2] = - self.velocity[2]
            if self.velocity[0] == 0.0:
                self.velocity[0] = 0.01
            if self.velocity[1] == 0.0:
                self.velocity[1] == 0.01

        for idx, c in enumerate(self.env_obj_list[1:]):
            if self.obj_id != c.obj_id:
                if (distance(self.bound_center, c.bound_center) <= (self.bound_radius + c.bound_radius)):
                    #self.setPreRotation(self.calcRotationMatrix())
                    self.velocity[0] = -self.velocity[0]
                    self.velocity[1] = -self.velocity[1]
                    self.velocity[2] = -self.velocity[2]

                    c.velocity[0] = -c.velocity[0]
                    c.velocity[1] = -c.velocity[1]
                    c.velocity[2] = -c.velocity[2]

                    
                    if (self.species_id > c.species_id):
                        collided_objects.append(c)
        #print(collided_objects)
        return collided_objects
                    #self.env_obj_list.remove(c)