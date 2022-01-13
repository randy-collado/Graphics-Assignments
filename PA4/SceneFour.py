"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import ColorType
from Animation import Animation
from Component import Component
from DIsplayableEllipsoid import DisplayableEllipsoid
from DisplayableCylinder import DisplayableCylinder
from Light import Light
from Material import Material
from Point import Point
import ColorType as Ct
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableTorus import DisplayableTorus

##### TODO 1: Generate Triangle Meshes
# Requirements:
#   1. Use Element Buffer Object (EBO) to draw the cube. The cube provided in the start code is drawn with Vertex Buffer
#   Object (VBO). In the DisplayableCube class draw method, you should switch from VBO draw to EBO draw. To achieve
#   this, please first read through VBO and EBO classes in GLBuffer. Then you rewrite the self.vertices and self.indices
#   in the DisplayableCube class. Once you have all these down, then switch the line vbo.draw() to ebo.draw().
#   2. Generate Displayable classes for an ellipsoid, torus, and cylinder with end caps.
#   These classes should be like the DisplayableCube class and they should all use EBO in the draw method.
#   PS: You must use the ellipsoid formula to generate it, scaling the Displayable sphere doesn't count
#
#   Displayable object's self.vertices numpy matrix should be defined as this table:
#   Column | 0:3                | 3:6           | 6:9          | 9:11
#   Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates
#
#   Their __init__ method should accept following input
#   arguments:
#   DisplayableEllipsoid(radiusInX, radiusInY, radiusInZ, slices, stacks)
#   DisplayableTorus(innerRadius, outerRadius, nsides, rings)
#   DisplayableCylinder(endRadius, height, slices, stacks)
#

##### TODO 5: Create your scenes
# Requirements:
#   1. We provide a fixed scene (SceneOne) for you with preset lights, material, and model parameters.
#   This scene will be used to examine your illumination implementation, and you should not modify it.
#   2. Create 3 new scenes (can be static scenes). Each of your scenes must have
#      * at least 3 differently shaped solid objects
#      * each object should have a different material
#      * at least 2 lights
#      * All types of lights should be used
#   3. Provide a keyboard interface that allows the user to toggle on/off each of the lights in your scene model:
#   Hit 1, 2, 3, 4, etc. to identify which light to toggle.


class SceneFour(Component):
    shaderProg = None
    glutility = None

    lights = None
    lightCubes = None
    light_registry = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0, 0, 0, 1)), 64)
        m2 = Material(np.array((0.3, 0.4, 0.7, 0.1)), np.array((0.2, 0.1, 0.1, 1)),
                      np.array((0, 0, 0, 1)), 64)

        m3 = Material(np.array((0.2, 0.1, 1.0, 0.1)), np.array((0.2, 0.7, 0.7, 1)),
                      np.array((0, 0, 0, 1)), 64)
        m4 = Material(np.array((0.2, 0.3, 0.4, 0.5)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0, 0, 0, 1)), 64)
        # cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.5, 1, 1.5))
        
        # cube.setMaterial(m1)
        # cube.renderingRouting = "lighting"
        # self.addChild(cube)

        main_cylinder_height = 1.0
        second_cylinder_height = 0.75
        third_cylinder_height = 0.50
        fourth_cylinder_height = 0.25

        base = 0
        downshift = -1.2

        cylinder = Component(Point((0, downshift, 0)), DisplayableCylinder(shaderProg, color=Ct.SOFTRED, height=main_cylinder_height))
        cylinder.setMaterial(m1)
        cylinder.renderingRouting = "lighting"
        cylinder.rotate(90, cylinder.uAxis)
        self.addChild(cylinder)
        base += main_cylinder_height/2
        cylinder2 = Component(Point((0, base + second_cylinder_height/2 + downshift, 0)), DisplayableCylinder(shaderProg, color=Ct.YELLOW, height=second_cylinder_height))
        cylinder2.setMaterial(m2)
        cylinder2.renderingRouting = "lighting"
        cylinder2.rotate(90, cylinder2.uAxis)
        self.addChild(cylinder2)
        base += second_cylinder_height
        cylinder3 = Component(Point((0, base + third_cylinder_height/2 + downshift, 0)), DisplayableCylinder(shaderProg, color=Ct.GREEN, height=third_cylinder_height))
        cylinder3.setMaterial(m3)
        cylinder3.renderingRouting = "lighting"
        cylinder3.rotate(90, cylinder3.uAxis)
        self.addChild(cylinder3)
        base += third_cylinder_height
        cylinder4 = Component(Point((0, base + fourth_cylinder_height/2 + downshift, 0)), DisplayableCylinder(shaderProg, color=Ct.ORANGE, height=fourth_cylinder_height))
        cylinder4.setMaterial(m4)
        cylinder4.renderingRouting = "lighting"
        cylinder4.rotate(90, cylinder4.uAxis)
        self.addChild(cylinder4)
        

        l0 = Light(Point([0.0, 1.5, 0.0]),
                   np.array((*ColorType.WHITE, 1.0)))
        lightCube0 = Component(Point((0.0, 1.5, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.lights = [l0, ]
        self.lightCubes = [lightCube0, ]
        self.light_registry = {
            l0: True
        }
    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()

    def toggleLights(self, key):
        key_digit = int(key)
        print(key_digit)
        if key_digit > len(self.lights):
            raise Exception("toggle key must be less than the number of lights!")
        else:
            self.shaderProg.clearAllLights()
            for i, v in enumerate(self.lights):
                if key_digit - 1 == i:
                    if self.light_registry[v]:
                        self.light_registry[v] = not self.light_registry[v]
                        print('toggled')
                        continue
                    else:
                        self.light_registry[v] = not self.light_registry[v]
                self.shaderProg.setLight(i, v)