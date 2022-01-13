"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1
"""

from Animation import Animation
from Component import Component
from Point import Point
import ColorType as Ct
from ModelLinkage import DisplayableCube


class ArmComponent(Component, Animation):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 

    components = None
    contextParent = None
    rightArm = False
    handWave = (-30, 30)

    def __init__(self, parent, position, rightArm=False, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.rightArm = rightArm
        self.wave_speed = 3
        color = Ct.ColorType(33/255, 37/255, 31/255)
        linkageLength = 0.5
        base = Component(Point((0, 0, 0)), DisplayableCube(self.contextParent, 1, [0.1, 0.1, linkageLength*0.9]))
        base.setDefaultColor(color)
        base.setRotateExtent(base.uAxis, -30, 30)
        #base.setRotateExtent(base.vAxis, 0, 10)
        base.setRotateExtent(base.wAxis, 0, 90)
        
        if rightArm:
            base.setDefaultAngle(base.vAxis, 180)
            base.rotate(25, base.uAxis)
        forearm = Component(Point((0, 0, linkageLength*0.9)), DisplayableCube(self.contextParent, 1, [0.1, 0.1, linkageLength*0.6]))
        forearm.setDefaultColor(color)
        if rightArm:
            forearm.rotate(-120, forearm.uAxis)
            forearm.setRotateExtent(forearm.uAxis, -140, -55)
        else:
            forearm.rotate(-40, forearm.uAxis)
            forearm.setRotateExtent(forearm.uAxis, -90, -5)
        hand = Component(Point((0, 0, linkageLength*0.6)), DisplayableCube(self.contextParent, 1, scale=[0.1, 0.2, 0.2]))
        hand.setDefaultColor(color)
        if rightArm:
            hand.setRotateExtent(hand.uAxis, *self.handWave)
            hand.setRotateExtent(hand.vAxis, -10, 90)
        else:
            hand.setRotateExtent(hand.uAxis, *self.handWave)
            hand.setRotateExtent(hand.vAxis, -10, 90)
            
        hand.setRotateExtent(hand.wAxis, -90, 90)

        self.addChild(base)
        base.addChild(forearm)
        forearm.addChild(hand)

        self.components = [base, forearm, hand]
        self.movable_components = [forearm]

    def animationUpdate(self):
        for c in self.movable_components:
            if self.rightArm:
                pass
                newAngle = c.uAngle + self.wave_speed
                if newAngle < -140 or newAngle > -55:
                    self.wave_speed = -self.wave_speed
                c.uAngle += self.wave_speed
            else:
                pass
                newAngle = c.uAngle + self.wave_speed
                if newAngle < -90 or newAngle > -5:
                    self.wave_speed = -self.wave_speed
                c.uAngle += self.wave_speed
        self.update()

