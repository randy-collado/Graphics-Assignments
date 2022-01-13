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
from DisplayableSphere import DisplayableSphere


class LegComponent(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 

    components = None
    contextParent = None
    rightLeg = False

    def __init__(self, parent, position, rightLeg=False, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.rightLeg = rightLeg

        linkageLength = 1
        base = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.1, 0.1, linkageLength*0.9]))
        base.setDefaultColor(Ct.DARKORANGE1)
        base.setDefaultAngle(90, base.uAxis)
        base.setRotateExtent(base.vAxis, -45, 45)
        base.setRotateExtent(base.uAxis, 0, 0)
        base.setRotateExtent(base.wAxis, 0, 0)

        # if rightLeg:
        #     base.rotate(15, base.uAxis)
        # else:
        #     base.rotate(-15, base.uAxis)
        calf = Component(Point((0, 0, linkageLength*0.9)), DisplayableCube(self.contextParent, 1, [0.1, 0.1, linkageLength*0.4]))
        calf.setDefaultColor(Ct.DARKORANGE2)
        calf.setRotateExtent(calf.uAxis, 0, 0)
        calf.setRotateExtent(calf.vAxis, 0, 90)
        calf.setRotateExtent(calf.wAxis, 0, 0)
        foot = Component(Point((0, 0, linkageLength*0.4)), DisplayableSphere(self.contextParent, radius=1, scale=[0.25, 0.25, 0.1]))
        foot.setDefaultColor(Ct.DARKORANGE3)
        

        self.addChild(base)
        base.addChild(calf)
        calf.addChild(foot)

        self.components = [base, calf, foot]

