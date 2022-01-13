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


class SceneTwo(Component):
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
                      np.array((0.4, 0.4, 0.4, 0.1)), 64)
        # cube = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 1.5, 1, 1.5))
        
        # cube.setMaterial(m1)
        # cube.renderingRouting = "lighting"
        # self.addChild(cube)

        ellipsoid = Component(Point((0, 0, 0)), DisplayableEllipsoid(shaderProg, 0.75, 0.75, 0.75, color=Ct.BLUE))
        ellipsoid.setMaterial(m1)
        ellipsoid.renderingRouting = "lighting"
        self.addChild(ellipsoid)

    
        torus = Component(Point((0, 0, 0)), DisplayableTorus(shaderProg, outerRadius=0.1, innerRadius=1.3, color=Ct.SILVER))
        torus.setMaterial(m1)
        torus.rotate(90, torus.uAxis)
        torus.renderingRouting = "lighting"
        self.addChild(torus)

        torus2 = Component(Point((0, 0, 0)), DisplayableTorus(shaderProg, outerRadius=0.1, innerRadius=1.3, color=Ct.SILVER))
        torus2.setMaterial(m1)
        torus2.rotate(90, torus2.uAxis)
        torus2.rotate(30, torus2.vAxis)
        torus2.renderingRouting = "lighting"
        self.addChild(torus2)

        torus3 = Component(Point((0, 0, 0)), DisplayableTorus(shaderProg, outerRadius=0.1, innerRadius=1.3, color=Ct.SILVER))
        torus3.setMaterial(m1)
        torus3.rotate(90, torus3.uAxis)
        torus3.rotate(-30, torus3.vAxis)
        torus3.renderingRouting = "lighting"
        self.addChild(torus3)

        l0 = Light(Point([0.0, 1.5, 0.0]),
                   np.array((*ColorType.WHITE, 1.0)))
        lightCube0 = Component(Point((0.0, 1.5, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"

        l1 = Light(Point([0.5, 1.5, 0.0]),
                   np.array((*ColorType.WHITE, 1.0)))

        self.addChild(lightCube0)
        self.lights = [l0, l1]
        self.lightCubes = [lightCube0, ]
        self.light_registry = {
            l0: True,
            l1: True
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