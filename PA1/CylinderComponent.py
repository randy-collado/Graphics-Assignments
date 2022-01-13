from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableCylinder import DisplayableCylinder


class CylinderComponent(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        cylinder: Component = Component(Point((0, 0, 0)), DisplayableCylinder(self.contextParent, height=0.5, topRadius=0.5, baseRadius=0.5, scale=[1, 1, 1]))
        cylinder.setDefaultColor(Ct.BLUE)
        self.addChild(cylinder)
        self.components = []

