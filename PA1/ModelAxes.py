"""
Create a x, y, z coordinate on canvas
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableCube import DisplayableCube


class ModelAxes(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        xAxis = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.05, 0.05, 2]))
        xAxis.rotate(90, xAxis.vAxis)
        xAxis.setDefaultColor(Ct.RED)
        xAxis.setDefaultAngle(90, xAxis.vAxis)
        yAxis = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.05, 0.05, 2]))
        yAxis.setDefaultAngle(-90, yAxis.uAxis)
        yAxis.setDefaultColor(Ct.GREEN)
        zAxis = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.05, 0.05, 2]))
        zAxis.setDefaultColor(Ct.BLUE)
        self.addChild(xAxis)
        self.addChild(yAxis)
        self.addChild(zAxis)

        self.components = []

