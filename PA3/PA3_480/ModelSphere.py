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
from SphereComponent import SphereComponent
from EnvironmentObject import EnvironmentObject
import math


class SphereCreature(Component, Animation, EnvironmentObject):
    radius = None
    components = []
    scale = None

    def __init__(self, parent, pos, radius=1, scale=[1, 1, 1], init_vel = [0.01, 0.01, 0.01], isPrey = True):
        position = pos
        self.radius = radius
        self.species_id = 1 if isPrey else 2
        self.obj_id = hash(self)
        self.scale = scale
        self.velocity = [0.01, 0.01, 0.01]
        self.bound_center = position
        self.bound_radius = 1
        super(SphereCreature, self).__init__(position)

        sphere = SphereComponent(parent, position=pos, radius=self.radius, scale=self.scale)
        self.addChild(sphere)
        self.components = sphere.components
        

    def animationUpdate(self):
        # for c in self.components:
        #     #print(c.current_position.getCoords())
        #     x, y, z = c.current_position.getCoords()
        #     x = x + 0.01
        #     #print(x)
        #     c.setCurrentPosition(Point((x, y, z)))
        #     c.bound_center = (Point((x, y, z)))
        self.update()
        

    def collision_detection(self):
        def distance(center_a: Point, center_b: Point):
            x1, y1, z1 = center_a.getCoords()
            x2, y2, z2 = center_b.getCoords()
            x_delta = (x2-x1)**2
            y_delta = (y2-y1)**2
            z_delta = (z2-z1)**2
            return math.sqrt(x_delta + y_delta + z_delta)

        collided_objects = []
        x = self.bound_center.coords[0]
        y = self.bound_center.coords[1]
        z = self.bound_center.coords[2]

        x_min = x - self.bound_radius
        x_max = x + self.bound_radius

        y_min = y - self.bound_radius
        y_max = y + self.bound_radius

        z_min = z - self.bound_radius
        z_max = z + self.bound_radius

        if (x_min <= -2.0 or x_max >= 2.0):
            self.velocity[0] = - self.velocity[0]
            if self.velocity[1] == 0.0:
                self.velocity[1] = 0.01
            if self.velocity[2] == 0.0:
                self.velocity[2] == 0.01
        if (y_min <= -2.0 or y_max >= 2.0):
            self.velocity[1] = - self.velocity[1]
            if self.velocity[0] == 0.0:
                self.velocity[0] = 0.01
            if self.velocity[2] == 0.0:
                self.velocity[2] == 0.01
        if (z_min <= -2.0 or z_max >= 2.0):
            self.velocity[2] = - self.velocity[2]
            if self.velocity[0] == 0.0:
                self.velocity[0] = 0.01
            if self.velocity[1] == 0.0:
                self.velocity[1] == 0.01

        for idx, c in enumerate(self.env_obj_list[1:]):
            if self.obj_id != c.obj_id:
                if (distance(self.bound_center, c.bound_center) <= (self.bound_radius + c.bound_radius)):
                    self.velocity[0] = -self.velocity[0]
                    self.velocity[1] = -self.velocity[1]
                    self.velocity[2] = -self.velocity[2]

                    c.velocity[0] = -c.velocity[0]
                    c.velocity[1] = -c.velocity[1]
                    c.velocity[2] = -c.velocity[2]

                    if (self.species_id > c.species_id):
                        collided_objects.append(c)
        print(collided_objects)
        return collided_objects
                    #self.env_obj_list.remove(c)
                    


