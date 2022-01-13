'''
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1
'''
import os
import wx
import time
import math
import random
import numpy as np
from ArmComponent import ArmComponent
from BodyComponent import BodyComponent
from CylinderComponent import CylinderComponent
from DisplayableSphere import DisplayableSphere
from Point import Point
import ColorType as CT
from ColorType import ColorType
from Quaternion import Quaternion
from Component import Component
#from DisplayableCube import DisplayableCube
from CanvasBase import CanvasBase
from ModelLinkage import ModelLinkage
from ModelAxes import ModelAxes
from SphereComponent import SphereComponent
from TailComponent import TailComponent
from LegComponent import LegComponent

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
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


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging

        
    Method Instruction:
        
        
    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
        
    Here are some public variables in parent class you might need:
        
        
    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    components = None
    select_obj_index = -1  # index in components
    select_axis_index = -1  # index of select axis
    select_color = [ColorType(1, 0, 0), ColorType(0, 1, 0), ColorType(0, 0, 1)]
    current_component_rotation_idx = []
    global_components = []

    def __init__(self, parent):
        """
        Init everything. You should set your model here.
        """
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        self.context = glcanvas.GLContext(self)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]

        ##### TODO 3: Import Your Creature
        # You should instance your creature class here, and add it as self.topLevelComponent's Child

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural way
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.

        
        self.components = []
        startpt = Point((0, 0.5, 0))
        arm_startpt = Point((0, 0.6, 0))
        rightleg_startpt = Point((0, 0.5, -0.2))
        leftleg_startpt = Point((0, 0.5, 0.2))
        #self.global_components.append(ModelAxes(self, Point((-1, -1, -1)))) # coordinate system with x, y, z axes
        #m2 = ModelLinkage(self, Point((0, 0, 0)))  # our model linkage (give it handle to parent object and attach it to objact i think)
       # global_components.append(SphereComponent(self, Point((0, 0.2, 0))))
        #m4 = CylinderComponent(self, Point((0, 1, 0)))
        #global_components.append(TailComponent(self, startpt))
        self.global_components.append(ArmComponent(self, arm_startpt))
        self.global_components.append(ArmComponent(self, arm_startpt, rightArm=True))
        self.global_components.append(BodyComponent(self, startpt))
        self.global_components.append(LegComponent(self, leftleg_startpt))
        self.global_components.append(LegComponent(self, rightleg_startpt, rightLeg=True))
        for components in self.global_components:
            self.topLevelComponent.addChild(components)
            self.components += components.components

    def Interrupt_Scroll(self, wheelRotation):
        """
        When mouse wheel rotating detected, do following things

        :param wheelRotation: mouse wheel changes, normally +120 or -120
        :return: None
        """
        wheelChange = wheelRotation / abs(wheelRotation)  # normalize wheel change
        if len(self.current_component_rotation_idx) <= 0:
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].rotate(wheelChange * 5,
                                                            self.components[self.select_obj_index].
                                                            axisBucket[self.select_axis_index])

        else:
            print(self.current_component_rotation_idx)
            for idx in self.current_component_rotation_idx:
                    if len(self.components) > idx >= 0:
                        self.global_components[idx].components[0].rotate(wheelChange * 5,
                                                                    self.global_components[idx].components[0].
                                                                    axisBucket[self.select_axis_index])
                        wheelChange = -wheelChange


        self.update()

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """
        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]
        mag = math.sqrt(dx * dx + dy * dy)
        axis = (dy / mag, -dx / mag, 0) if mag != 0 else (1, 0, 0)
        viewing_delta = 3.14159265358 / 180
        s = math.sin(0.5 * viewing_delta)
        c = math.cos(0.5 * viewing_delta)
        q = Quaternion(c, s * axis[0], s * axis[1], s * axis[2])
        self.viewing_quaternion = q.multiply(self.viewing_quaternion)
        self.viewing_quaternion.normalize()  # to correct round-off error caused by cos/sin
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.modelUpdate()

    def Interrupt_MouseMoving(self, x, y):
        ##### BONUS 2 (TODO 6 for CS680 student): Finishing touch - eyes!
        # Requirements:
        #   1. Add eyes to the creature model, for each it consists of an eyeball and pupil.
        #   2. Make eyes automatically follow the mouse position by rotating the eyeball.
        #   3. (extra credits) Use quaternion to implement the eyeball rotation
        pass

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """
        
            # for c in self.components:
            #     c.firstPose()


        if keycode in [wx.WXK_RETURN]:
            # enter component editing mode
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].reset("color")

            self.select_axis_index = 0
            if len(self.components) > 0:
                if self.select_obj_index < 0:
                    self.select_obj_index = 0
                else:
                    self.select_obj_index = (self.select_obj_index + 1) % len(self.components)

            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_LEFT]:
            # Last rotation axis of this component
            self.select_axis_index = (self.select_axis_index - 1) % 3
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_RIGHT]:
            # Next rotation axis of this component
            self.select_axis_index = (self.select_axis_index + 1) % 3
            if len(self.components) > self.select_obj_index >= 0:
                if len(self.current_component_rotation_idx) <= 0:
                    self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
                else:
                    for idx in self.current_component_rotation_idx:
                        self.global_components[idx].components[0].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_UP]:
            # Increase rotation angle
            self.Interrupt_Scroll(1)
            self.update()
        if keycode in [wx.WXK_DOWN]:
            # Decrease rotation angle
            self.Interrupt_Scroll(-1)
            self.update()
        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            if len(self.components) > self.select_obj_index >= 0:
                self.components[self.select_obj_index].reset("color")
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()
        if chr(keycode) in "r":
            # reset viewing angle only
            self.viewing_quaternion = Quaternion()
        if chr(keycode) in "R":
            # reset everything
            for c in self.components:
                c.reset()
            self.viewing_quaternion = Quaternion()
            self.select_obj_index = 0
            self.select_axis_index = 0
            self.update()
        if chr(keycode) == '1':
            self.multiSelect(1)
        if chr(keycode) == '2':
            self.multiSelect(ArmComponent)
        if chr(keycode) == '3':
            self.multiSelect(LegComponent)
        if chr(keycode) == '4':
            pass#self.multiSelect(4)
        if chr(keycode) == '5':
            pass#self.multiSelect(5)
        if chr(keycode) == 't':
            pass

    def multiSelect(self, componentType):
        print(self.global_components)
        self.current_component_rotation_idx = []
        for i in range(len(self.components)):
            self.components[i].reset('color')
        for j in range(len(self.global_components)):
            if type(self.global_components[j]) is componentType:
                print('hehe')
                self.global_components[j].components[0].setCurrentColor(self.select_color[self.select_axis_index])
                self.current_component_rotation_idx.append(j)

        self.update()

if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
