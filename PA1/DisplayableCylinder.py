'''
A test object which defines a primitive shape for rendering
All primitive shapes must inherit from Displayable class
First version in 10/21/2018

:author: micou(Zezhou Sun)/randy64(Randy Collado)
:version: 2021.1.1
'''
import os
import numpy as np
import string

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut  # this fails on OS X 11.x
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
        import OpenGL.GLUT as glut
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError

from Displayable import Displayable


class DisplayableCylinder(Displayable):
    """
    Create a enclosed cylinder whose one end is at z=0 and it grows along z coordinates
    """

    ##### TODO 1: Build Creature Parts
    # Build the class(es) of basic geometric objects/combination that could add up to be a part of your creature. 
    # E.g., you could write a cylinder class to be the trunk of your creature's limb. Or, you could 
    # write a two-sphere class to be the eye ball of your creature (one sphere for the eye ball and one sphere for the lens/iris).
    # The needed GLU functions for cylinder and sphere are mentioned in README.md



    callListHandle = 0  # long int. override the one in Displayable
    qd = None  # Quadric
    #sphere = None
    scale = None
    height = 1
    topRadius = 1
    baseRadius = 1
    _bufferData = None
    slices: int
    stacks: int
    slices, stacks = 36, 36

    def __init__(self, parent, height=height, topRadius=topRadius, baseRadius=baseRadius, scale=None):
        super().__init__(parent)
        parent.context.SetCurrent(parent)
        self.height = height 
        self.topRadius = topRadius
        self.baseRadius = baseRadius
        if scale is None:
            scale = [1, 1, 1]
        self.scale = scale

    ##### BONUS 1: Texture your creature
    # Requirement: 1. Build the texture mapping that binds texture image to your objects. 

    def draw(self):
        glu.gluCylinder(self.qd, self.baseRadius, self.topRadius, self.height, self.slices, self.stacks)

    def initialize(self):
        self.callListHandle = gl.glGenLists(1)
        self.qd = glu.gluNewQuadric()