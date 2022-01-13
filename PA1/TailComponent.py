"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableCube import DisplayableCube


class TailComponent(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        colors = [Ct.DARKORANGE3, Ct.GARFIELD_ORANGE]

        linkageWidth = 0.1
        linkageHeight = 0.1
        linkageLength = 0.5
        linkages = 8
        childComponents = False
        
        for i in range(linkages):
            if not childComponents:
                c = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [linkageWidth, linkageHeight, linkageLength]))
                c.setDefaultAngle(90, c.vAxis)
                self.addChild(c)
                childComponents = True
            else:
                c = Component(Point((0, 0, linkageLength/i)), DisplayableCube(self.contextParent, 1, [linkageWidth, linkageHeight, linkageLength/(i+1)]))
                c.rotate(-10, c.uAxis)
                self.components[i-1].addChild(c)
            c.setDefaultColor(colors[i%len(colors)])
            self.components.append(c)
        self.components = [self.components[0]]

        # link1 = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        # link1.setDefaultColor(Ct.DARKORANGE2)
        # link1.setDefaultAngle(90, link1.vAxis)
        # link2 = Component(Point((0, 0, linkageLength)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        # link2.setDefaultColor(Ct.DARKORANGE2*0.33)
        # link2.rotate(-30, link2.uAxis)
        # print(Ct.DARKORANGE2*0.66 + Ct.RED*0.33)
        # link3 = Component(Point((0, 0, linkageLength)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        # link3.setDefaultColor(Ct.DARKORANGE2*0.66)
        # link3.rotate(-30, link3.uAxis)
        # link4 = Component(Point((0, 0, linkageLength)), DisplayableCube(self.contextParent, 1, [0.2, 0.2, linkageLength]))
        # link4.setDefaultColor(Ct.RED)
        # link4.rotate(-30, link4.uAxis)

        # self.addChild(link1)
        # link1.addChild(link2)
        # link2.addChild(link3)
        # link3.addChild(link4)

        # self.components = [link1, link2, link3, link4]

