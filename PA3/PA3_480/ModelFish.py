"""
My fish object, created from a body, a tail fin, and a dorsal finn.

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import random
from ModelLinkage import DisplayableCube

from Point import Point
from Component import Component
from Animation import Animation
from SphereComponent import SphereComponent
from EnvironmentObject import EnvironmentObject
import ColorType as Ct
import math
import numpy as np

from TriPrismComponent import TriPrismComponent


class FishCreature(Component, Animation, EnvironmentObject):
    radius = None
    components = []
    scale = None

    def __init__(self, parent, pos, scale=1, init_vel = [0.07, 0.03, 0.01], isPrey = True):
        position = pos
        self.species_id = 1 if isPrey else 2 #robot is 3 -> robot eats red and green fish, red fish eat green fish
        self.obj_id = hash(self) #this ensures that each creatures obj_id is unique
        self.scale = scale
        self.velocity = init_vel
        self.bound_center = pos
        self.bound_radius = 0.7*scale
        self.noRotation = [0, 0]
        self.flap_speed = 2
        self.colors = {"tail": Ct.ORANGE, "finn":Ct.DARKORANGE2, "body":Ct.RED} if not isPrey else {"tail": Ct.GREENYELLOW, "finn": Ct.GREEN, "body": Ct.DARKGREEN}
        #lets me dynamically choose colors based on which type of animal.
        super(FishCreature, self).__init__(pos)

        body = SphereComponent(parent, position=pos, radius=1, scale=[0.40*scale, 0.60*scale, 0.40*scale], color=self.colors["body"])
        body.setDefaultAngle(body.wAxis, 90)

        t = TriPrismComponent(parent, position=Point((0, -0.8, 0.5)), scale=[0.5, 1, 1], color=self.colors["tail"])
        t.setDefaultAngle(t.uAxis, -45)

        t.rotate#(90, t.wAxis)
        t.setCurrentColor(Ct.BLUE)

        tail = Component(Point((0, -0.3, -0.05)), DisplayableCube(parent, 1, [0.4*scale, 0.4*scale, 0.1*scale]))
        tail.setCurrentColor(self.colors["tail"])
        #tail.setU([0.6, 0, 0])

        finn = Component(Point((0.15, 0, 0)), DisplayableCube(parent, 1, [0.30*scale, 0.4*scale, 0.1*scale]))
        finn.setDefaultAngle(finn.wAxis, 20)
        finn.setCurrentColor(self.colors["finn"])
        


        body.addChild(tail)
        body.addChild(finn)
        #body.addChild(t)
        self.addChild(body)
        self.components = [tail]
        

    def animationUpdate(self):
        '''
        flaps the finn left and right
        '''
        for c in self.components:
            if c.uAngle + self.flap_speed < -45:
                self.flap_speed = -self.flap_speed
            if c.uAngle + self.flap_speed > 45:
                self.flap_speed = -self.flap_speed
            c.rotate(self.flap_speed, c.uAxis)
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
                    


