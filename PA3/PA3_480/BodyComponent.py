from wx.core import Right
from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableSphere import DisplayableSphere


class BodyComponent(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None
    torso_radius = 0.25
    head_radius = 0.15
    eye_radius = 0.0075
    eye_offset = 0.05
    startpt = Point((0, 1, 0))
    noRotation = [0, 0]

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        color = Ct.ColorType(33/255, 37/255, 31/255)
        eye_color = Ct.ColorType(214/255, 233/255, 39/255)
        torso: Component = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, radius=self.torso_radius, scale=[1, 1.2, 1]))
        torso.setDefaultColor(color)
        torso.setRotateExtent(torso.uAxis, *self.noRotation)
        torso.setRotateExtent(torso.vAxis, *self.noRotation)
        torso.setRotateExtent(torso.wAxis, -90, 5)

        head: Component = Component(Point((0, self.torso_radius, 0)), DisplayableSphere(self.contextParent, radius=self.head_radius, scale=[1, 1, 1]))
        head.setDefaultColor(color)
        head.setRotateExtent(head.uAxis, -30, 30)
        head.setRotateExtent(head.vAxis, -120, 120)
        head.setRotateExtent(head.wAxis, *self.noRotation)

        left_eye: Component = Component(Point((-self.head_radius, self.eye_offset, self.eye_offset)), DisplayableSphere(self.contextParent, radius=self.eye_radius, scale=[1, 1, 1]))
        left_eye.setRotateExtent(head.uAxis, *self.noRotation)
        left_eye.setRotateExtent(head.vAxis, *self.noRotation)
        left_eye.setRotateExtent(head.wAxis, *self.noRotation)
        left_eye.setDefaultColor(eye_color)
        head.addChild(left_eye)
        
        right_eye: Component = Component(Point((-self.head_radius, self.eye_offset, -self.eye_offset)), DisplayableSphere(self.contextParent, radius=self.eye_radius, scale=[1, 1, 1]))
        right_eye.setRotateExtent(head.uAxis, *self.noRotation)
        right_eye.setRotateExtent(head.vAxis, *self.noRotation)
        right_eye.setRotateExtent(head.wAxis, *self.noRotation)
        right_eye.setDefaultColor(eye_color)
        head.addChild(right_eye)
        
        
        self.addChild(torso)
        torso.addChild(head)
        self.components = [head, torso]

