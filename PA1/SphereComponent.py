from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableSphere import DisplayableSphere


class SphereComponent(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        sphere: Component = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, radius=0.5, scale=[1, 1, 1]))
        sphere.setDefaultColor(Ct.DARKORANGE2)
        self.addChild(sphere)
        self.components = []

