"""
This is the main entry of your program. Almost all things you need to implement is in this file.
The main class Sketch inherit from CanvasBase. For the parts you need to implement, they all marked TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1

"""

"""
Name: Randy Collado-Cedeno
Course: CS480
Assignment Number: 1
Due Date: Septamber 22nd, 2021
Collaborators: None

This code is a demo of line and triangle rasterization using Bresenham's line-rasterization algorithm
and scanfill-coloring triangles. This is done throuhg two functions drawLine and drawTriangle, which take as input 
a buffer and two points (3 points for the triangle) as well as flags whether to enable smooth interpolated coloring.

Error conditions: currently, there are two errors in this source code.
1: Bilinear interpolation for triangle colors does interpolate smoothly, but flips the colors of the triangle by 
60 degrees in cases where the triangle is drawn with the apex first
2. Test-case 2 outputs a divide by 0 error once the number of steps increases beyond 96
"""

import os

import wx
import math
import random
import numpy as np

from Buff import Buff
from Point import Point
from ColorType import ColorType
from CanvasBase import CanvasBase

try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    """
    Please don't forget to override interrupt methods, otherwise NotImplementedError will throw out
    
    Class Variable Explanation:

    * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging
    
    * texture(Buff): loaded texture in Buff instance
    * random_color(bool): Control flag of random color generation of point.
    * doTexture(bool): Control flag of doing texture mapping
    * doSmooth(bool): Control flag of doing smooth
    * doAA(bool): Control flag of doing anti-aliasing
    * doAAlevel(int): anti-alising super sampling level
        
    Method Instruction:

    * Interrupt_MouseL(R): Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
    * Interrupt_Keyboard: Used to deal with key board press interruption. Use this to add new keys or new methods
    * drawPoint: method to draw a point
    * drawLine: method to draw a line
    * drawTriangle: method to draw a triangle with filling and smoothing
    
    List of methods to override the ones in CanvasBase:

    * Interrupt_MouseL
    * Interrupt_MouseR
    * Interrupt_Keyboard
        
    Here are some public variables in parent class you might need:

    * points_r: list<Point>. to store all Points from Mouse Right Button
    * points_l: list<Point>. to store all Points from Mouse Left Button
    * buff    : Buff. buff of current frame. Change on it will change display on screen
    * buff_last: Buff. Last frame buffer
        
    """

    debug = 0
    texture_file_path = "./pattern.jpg"
    texture = None

    # control flags
    randomColor = False
    doTexture = False
    doSmooth = False
    doAA = False
    doAAlevel = 4

    # test case status
    MIN_N_STEPS = 6
    MAX_N_STEPS = 192
    n_steps = 12  # For test case only
    test_case_index = 0
    test_case_list = []  # If you need more test case, write them as a method and add it to list

    def __init__(self, parent):
        """
        Initialize the instance, load texture file to Buff, and load test cases.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        self.test_case_list = [lambda _: self.clear(),
                               self.testCaseLine01,
                               self.testCaseLine02,
                               self.testCaseTri01,
                               self.testCaseTri02,
                               self.testCaseTriTexture01]  # method at here must accept one argument, n_steps
        # Try to read texture file
        if os.path.isfile(self.texture_file_path):
            # Read image and make it to an ndarray
            texture_image = Image.open(self.texture_file_path)
            texture_array = np.array(texture_image).astype(np.uint8)
            # Because imported image is upside down, reverse it
            texture_array = np.flip(texture_array, axis=0)
            # Store texture image in our Buff format
            self.texture = Buff(texture_array.shape[1], texture_array.shape[0])
            self.texture.setStaticBuffArray(np.transpose(texture_array, (1, 0, 2)))
            if self.debug > 0:
                print("Texture Loaded with shape: ", texture_array.shape)
                print("Texture Buff have size: ", self.texture.size)
        else:
            raise ImportError("Cannot import texture file")

    def __addPoint2Pointlist(self, pointlist, x, y):
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)

    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x, y):
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point provided or a line when two ends provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.drawPoint(self.buff, self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-1], " -> ", self.points_l[-2])
            self.drawPoint(self.buff, self.points_l[-1])
            # TODO: new line to test the drawLine function
            self.drawLine(self.buff, self.points_l[-2], self.points_l[-1])
            #self.drawRectangle(self.buff, self.points_l[-2], self.points_l[-1])
            self.points_l.clear()

    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x, y):
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 3 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a triangle {} -> {} -> {}".format(self.points_r[-3], self.points_r[-2], self.points_r[-1]))
            self.drawTriangle(self.buff, self.points_r[-3], self.points_r[-2], self.points_r[-1])
            self.points_r.clear()

    def Interrupt_Keyboard(self, keycode):
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screen
        * LEFT, UP: Last Test case
        * t, T, RIGHT, DOWN: Next Test case
        """
        # Trigger for test cases
        if keycode in [wx.WXK_LEFT, wx.WXK_UP]:  # Last Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index - 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [ord("t"), ord("T"), wx.WXK_RIGHT, wx.WXK_DOWN]:  # Next Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ",<":
            self.clear()
            self.n_steps = max(self.MIN_N_STEPS, round(self.n_steps / 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ".>":
            self.clear()
            self.n_steps = min(self.MAX_N_STEPS, round(self.n_steps * 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)

        # Switches
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if self.debug > 1:
            if x != min(max(0, int(x)), texture.width - 1):
                print("Warning: Texture Query x coordinate outbound")
            if y != min(max(0, int(y)), texture.height - 1):
                print("Warning: Texture Query y coordinate outbound")
        return texture.getPointFromPointArray(x, y)

    @staticmethod
    def drawPoint(buff, point):
        """
        Draw a point on buff

        :param buff: The buff to draw point on
        :type buff: Buff
        :param point: A point to draw on buff
        :type point: Point
        :rtype: None
        """
        x, y = point.coords
        c = point.color
        # because we have already specified buff.buff has data type uint8, type conversion will be done in numpy
        buff.buff[x, y, 0] = c.r * 255
        buff.buff[x, y, 1] = c.g * 255
        buff.buff[x, y, 2] = c.b * 255

    def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Draw a line between p1 and p2 on buff

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: None
        """

        # Bresenham's Decision parameter: D_k+1 = D_k + 2delta(y) - 2delta(x)[(y_k+1 - y_k) -> either 0 or 1]
        x1, y1 = p1.coords
        x2, y2 = p2.coords

        r1, g1, b1 = p1.color.getRGB()
        r2, g2, b2 = p2.color.getRGB()

        dx = abs(x2 - x1)   
        dy = abs(y2 - y1)

        y_dominant = False

        #in the case that the change in y is greater than the change in x, 
        if dy > dx: #^ coordSwap:
            swap = dx
            dx = dy
            dy = swap
            y_dominant = True
        
        #in the case that the points are chosen right to left, a swap is needed in order to preserve the behavior of drawing
        #left to right, this limits the amount of branching needed in the code (reference commented code for reference)
        if (x2 - x1) < 0:
            x1, y1 = p2.coords
            x2, y2 = p1.coords
            r1, g1, b1 = p1.color.getRGB()
            r2, g2, b2 = p2.color.getRGB()

        y_delta = int(math.copysign(1, y2-y1))
        x_delta = int(math.copysign(1, x2-x1))
        #print(signX)

        x = x1
        y = y1
        
        D = 2*dy - dx
        for i in range(dx):
            #calculates color data in the case of smooth coloring
            if doSmooth:
                if x1 == x2:
                    c = y
                    c1 = y1
                    c2 = y2
                else:
                    c = x
                    c1 = x1
                    c2 = x2
                alpha = Sketch.get_alpha_from_lerp(c, c1, c2)
                c = ColorType(Sketch.lerp(alpha=alpha, x_0=r1, x_1=r2), Sketch.lerp(alpha=alpha, x_0=g1, x_1=g2), Sketch.lerp(alpha=alpha, x_0=b1, x_1=b2))
            else:
                c = p1.color

            Sketch.drawPoint(buff, Point(coords=(x, y), color=c))
            
            #If the decision parameter is greater than 0, then we color the next pixel above 
            #(or beside our current position in the case that the line is y_dominant)
            #otherwise, we color the current position in the next iteration
            if D >= 0:
                #the swap accounts for the case that the change in y is greater 
                #than the change in x
                if y_dominant:
                    x += (1 if x_delta == 1 else -1)
                else:
                    y += (1 if y_delta == 1 else -1) 
                D -= 2*dx
            
            #this step moves our imaginary paintbrush forward along the line, by y if the line is y-dominant;
            #incrementing x otherwise
            if y_dominant:
                y += y_delta 
            else:
                x += x_delta 
            D += 2*dy
        
        # elif dy >= dx: #m > 1:
        #     D = 2*dx - dy
        #     print(f'dx: {dx}\ndy: {dy}')
        #     #print("here")
            
        #     for i in range(dy + 1):
        #         alpha = Sketch.get_alpha_from_lerp(y, y1, y2)
        #         c = ColorType(Sketch.lerp(alpha=alpha, x_0=r1, x_1=r2), Sketch.lerp(alpha=alpha, x_0=g1, x_1=g2), Sketch.lerp(alpha=alpha, x_0=b1, x_1=b2))
        #         Sketch.drawPoint(buff, Point(coords=(x, y), color=c))
        #         print(D)
        #         if D > 0:
        #             D -= 2*dy 
        #             x += 1

        #         if D < 0:
        #             #issue: for lines with negative slope, D gets very negative
        #             D += 2*dy 
        #             x -= 1
        #             #print(D)

        #         D += 2*dx
                
        #         y += 1


        #TODO: fix bug with lines with slopes btwn 0 and negative 1 with extremely negative 

    #WORKS, but need to fix line issue ASAP
    def scanfill_bottomflat_tri(self, buff: Buff, p1: Point, p2: Point, p3: Point):
        """
        Logic extracted out for scanfilling a bottom-flat triangle, inspiration from Triangle Rasterization tutorial
        """
        p1, p2, p3 = Sketch.sortByAscendingY(p1, p2, p3)

        x1, y1 = p1.coords
        x2, y2 = p2.coords
        x3, y3 = p3.coords

        r1, g1, b1 = p1.color.getRGB()
        r2, g2, b2 = p2.color.getRGB()
        r3, g3, b3 = p3.color.getRGB()
        
        for i in range(y1, y2):

            #calculates the distance we're at relative to the sides of the triangle
            alpha_12 = Sketch.get_alpha_from_lerp(i, y1, y2)
            alpha_13 = Sketch.get_alpha_from_lerp(i, y1, y3)

            #linear interpolates along the sides of the triangle in order to find the app
            c1  = ColorType(Sketch.lerp(alpha=alpha_13, x_0=r1, x_1=r3), Sketch.lerp(alpha=alpha_13, x_0=g1, x_1=g3), Sketch.lerp(alpha=alpha_13, x_0=b1, x_1=b3))
            c2 = ColorType(Sketch.lerp(alpha=alpha_12, x_0=r1, x_1=r2), Sketch.lerp(alpha=alpha_12, x_0=g1, x_1=g2), Sketch.lerp(alpha=alpha_12, x_0=b1, x_1=b2))

            #similarly, interpolates along the edges to find the current x-locations of the achor points of the line
            current_x0 = Sketch.lerp(x1, x3, alpha_13)
            current_x1 = Sketch.lerp(x1, x2, alpha_12)

            #the line function itself is responsible for interpolating between these two colors
            self.drawLine(buff, Point(coords=(int(current_x0), i), color=c2), Point(coords=(int(current_x1), i), color=c1))

    def scanfill_topflat_tri(self, buff: Buff, p1: Point, p2: Point, p3: Point):
        """
        Logic extracted out for scanfilling a top-flat triangle, inspiration from Triangle Rasterization tutorial
        """
        p1, p2, p3 = Sketch.sortByDescendingY(p1, p2, p3)
        x1, y1 = p1.coords
        x2, y2 = p2.coords
        x3, y3 = p3.coords

        r1, g1, b1 = p1.color.getRGB()
        r2, g2, b2 = p2.color.getRGB()
        r3, g3, b3 = p3.color.getRGB()

        #debug line
        #print('yoohoo', y1, y2, y3)

        for i in range(y1, y3):
            #calculates the distance we're at relative to the sides of the triangle
            alpha_23 = Sketch.get_alpha_from_lerp(i, y2, y3)
            alpha_13 = Sketch.get_alpha_from_lerp(i, y1, y3)

            #linear interpolation of the colors at each of the endpoints on the triangle
            c1  = ColorType(Sketch.lerp(alpha=alpha_13, x_0=r1, x_1=r3), Sketch.lerp(alpha=alpha_13, x_0=g1, x_1=g3), Sketch.lerp(alpha=alpha_13, x_0=b1, x_1=b3))
            c2 = ColorType(Sketch.lerp(alpha=alpha_23, x_0=r2, x_1=r3), Sketch.lerp(alpha=alpha_23, x_0=g2, x_1=g3), Sketch.lerp(alpha=alpha_23, x_0=b2, x_1=b3))

            #linear interpolates along the sides of the triangle in order to find the app
            current_x0 = Sketch.lerp(x1, x3, Sketch.get_alpha_from_lerp(i, y1, y3))
            current_x1 = Sketch.lerp(x2, x3, Sketch.get_alpha_from_lerp(i, y2, y3))
            
            #the line function itself is responsible for interpolating between these two colors
            self.drawLine(buff, Point(coords=(int(current_x1), i), color=c1), Point(coords=(int(current_x0), i), color=c2))


    def drawTriangle(self, buff, p1, p2, p3, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False):
        """
        draw Triangle to buff. apply smooth color filling if doSmooth set to true, otherwise fill with first point color
        if doAA is true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: First triangle vertex
        :param p2: Second triangle vertex
        :param p3: Third triangle vertex
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """
        ##### TODO 2: Write a triangle rendering function, which support smooth bilinear interpolation of the vertex color
        p1, p2, p3 = Sketch.sortByAscendingY(p1, p2, p3)
        x1, y1 = p1.coords
        x2, y2 = p2.coords
        x3, y3 = p3.coords
        bPoint = Sketch.calcBoundaryPoint(p1, p2, p3)

        #print(bPoint.coords)
        if y1 == y2:
            self.scanfill_topflat_tri(buff, p1, p2, p3)
        elif y2 == y3:
            self.scanfill_bottomflat_tri(buff, p1, p2, p3)
        else:
            #print('triggered')
            self.scanfill_topflat_tri(buff, p1, bPoint, p2)
            #print('second triggered')
            self.scanfill_bottomflat_tri(buff, bPoint, p2, p3)
        #TODO: add bilinear interpolation
        ##### TODO 3(For CS680 Students): Implement texture-mapped fill of triangle. Texture is stored in self.texture
        # Requirements:
        #   1. For flat shading of the triangle, use the first vertex color.
        #   2. Polygon scan fill algorithm and the use of barycentric coordinate are not allowed in this function
        #   3. You should be able to support both flat shading and smooth shading, which is controlled by doSmooth
        #   4. For texture-mapped fill of triangles, it should be controlled by doTexture flag.
#------------------------------utility functions---------------------------------------#
    
    @staticmethod
    def calcBoundaryPoint(p1, p2, p3) -> Point:
        """
        calculates the boundary point for which the triangle is divided on in order to split it into top-flat
        and bottom-flat triangles
        """
        # sorts the 3 points by y, so we are certain that y2 is the middle point relative to y
        p1, p2, p3 = Sketch.sortByAscendingY(p1, p2, p3)

        x1, y1 = p1.coords
        x2, y2 = p2.coords
        x3, y3 = p3.coords

        #the color of the boundary point is the lerp of the colors of the points on which the boundary lies
        r1, g1, b1 = p1.color.getRGB()
        r3, g3, b3 = p3.color.getRGB()
        b_point_alpha = Sketch.get_alpha_from_lerp(y2, y1, y3)
        b_point_color = ColorType(Sketch.lerp(r1, r3, b_point_alpha), Sketch.lerp(g1, g3, b_point_alpha), Sketch.lerp(b1, b3, b_point_alpha))
        
        midY = y2
        
        #the x-component is calculated from the alpha given the y-components
        midX = Sketch.lerp(x1, x3, b_point_alpha)
        return Point(coords=(int(midX), midY), color=b_point_color)

    @staticmethod
    def lerp(x_0, x_1, alpha):
        """
        utility function to calculate the lerp of any two values given alpha
        """
        return (1-alpha)*x_0 + alpha*x_1

    def get_alpha_from_lerp(y, y_0, y_1):
        """
        utility function to calculate alpha (for lerp) given a point y(t) 
        and two endpoints y_0 and y_1
        """
        return (y-y_0)/(y_1-y_0)

    @staticmethod
    def sortByAscendingY(p1, p2, p3):
        """
        sorts 3 given points by their y-components from highest to lowest 
        (confusing wording I know)
        """
        y1 = p1.coords[1]
        y2 = p2.coords[1]
        y3 = p3.coords[1]
        if y1 > y2 and y1 > y3:
            if y2 > y3:
                return p1, p2, p3
            else:
                return p1, p3, p2
        elif y2 > y1 and y2 > y3:
            if y1 > y3:
                return p2, p1, p3
            else:
                return p2, p3, p1
        else:
            if y1 > y2:
                return p3, p1, p2
            else:
                return p3, p2, p1

    @staticmethod
    def sortByDescendingY(p1, p2, p3):
        """
        sorts 3 given points by their y-components from lowest to highest
        (confusing wording I know)
        """
        y1 = p1.coords[1]
        y2 = p2.coords[1]
        y3 = p3.coords[1]
        if y1 < y2 and y1 < y3:
            if y2 < y3:
                return p1, p2, p3
            else:
                return p1, p3, p2
        elif y2 < y1 and y2 < y3:
            if y1 < y3:
                return p2, p1, p3
            else:
                return p2, p3, p1
        else:
            if y1 < y2:
                return p3, p1, p2
            else:
                return p3, p2, p1

#---------------------------------------------------------------------------------------#

    def drawRectangle(self, buff, p1, p2):
        x1, y1 = p1.coords
        x2, y2 = p2.coords

        ymax = max(y1, y2)
        ymin = min(y1, y2)

        xmax = max(x1, x2)
        xmin = min(x1, x2)

        for i in range(xmin, xmax+1):
            for j in range(ymin, ymax+1):
                Sketch.drawPoint(buff, Point(coords=(i, j), color=p1.color))

        
    # test for lines lines in all directions
    def testCaseLine01(self, n_steps):
        center_x = int(self.buff.width / 2)
        center_y = int(self.buff.height / 2)
        radius = int(min(self.buff.width, self.buff.height) * 0.45)

        v0 = Point([center_x, center_y], ColorType(1, 1, 0))
        for step in range(0, n_steps):
            theta = math.pi * step / n_steps
            v1 = Point([center_x + int(math.sin(theta) * radius), center_y + int(math.cos(theta) * radius)],
                       ColorType(0, 0, (1 - step / n_steps)))
            v2 = Point([center_x - int(math.sin(theta) * radius), center_y - int(math.cos(theta) * radius)],
                       ColorType(0, (1 - step / n_steps), 0))
            self.drawLine(self.buff, v2, v0, doSmooth=True)
            self.drawLine(self.buff, v0, v1, doSmooth=True)

    # test for lines: drawing circle and petal 
    def testCaseLine02(self, n_steps):
        n_steps = 2 * n_steps
        d_theta = 2 * math.pi / n_steps
        d_petal = 12 * math.pi / n_steps
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        radius = (0.75 * min(cx, cy))
        p = radius * 0.25

        # Outer petals
        for i in range(n_steps + 2):
            self.drawLine(self.buff,
                          Point((math.floor(0.5 + radius * math.sin(d_theta * i) + p * math.sin(d_petal * i)) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * i) + p * math.cos(d_petal * i)) + cy),
                                ColorType(1, (128 + math.sin(d_theta * i * 5) * 127 / 255),
                                          (128 + math.cos(d_theta * i * 5) * 127 / 255))),
                          Point((math.floor(
                              0.5 + radius * math.sin(d_theta * (i + 1)) + p * math.sin(d_petal * (i + 1))) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * (i + 1)) + p * math.cos(
                                     d_petal * (i + 1))) + cy),
                                ColorType(1, (128 + math.sin(d_theta * 5 * (i + 1)) * 127 / 255),
                                          (128 + math.cos(d_theta * 5 * (i + 1)) * 127 / 255))),
                          doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

        # Draw circle
        for i in range(n_steps + 1):
            v0 = Point((math.floor(0.5 * radius * math.sin(d_theta * i)) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * i)) + cy), ColorType(1, 97. / 255, 0))
            v1 = Point((math.floor(0.5 * radius * math.sin(d_theta * (i + 1))) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * (i + 1))) + cy), ColorType(1, 97. / 255, 0))
            self.drawLine(self.buff, v0, v1, doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

    # test for smooth filling triangle
    def testCaseTri01(self, n_steps):
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v1, v0, v2, False, self.doAA, self.doAAlevel)

    def testCaseTri02(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v0, v1, v2, True, self.doAA, self.doAAlevel)

    def testCaseTriTexture01(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        triangleList = []
        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            triangleList.append([v0, v1, v2])

        for t in triangleList:
            self.drawTriangle(self.buff, *t, doTexture=True)


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)

        canvas = Sketch(frame)
        canvas.debug = 0

        frame.Show()
        app.MainLoop()


    def codingDebug():
        """
        If you are still working on the assignment, we suggest to use this as the main call.
        There will be more strict type checking in this version, which might help in locating your bugs.
        """
        print("This is the debug entry! ")
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        canvas = Sketch(frame)
        canvas.debug = 2
        frame.Show()
        app.MainLoop()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
        stats.print_stats()


    main()
    #codingDebug()
