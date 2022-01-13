from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableSphere import DisplayableSphere


class SphereComponent(Component):
    """
    Define our Sphere model
    """

    components = None
    contextParent = None
    radius = None
    position = None
    scale = None

    def __init__(self, parent, radius, position, scale, color, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.position = position
        self.radius = radius
        self.scale = scale

        sphere: Component = Component(Point((0, 0, 0)), DisplayableSphere(self.contextParent, radius=self.radius, scale=self.scale))
        sphere.setDefaultColor(color)
        self.addChild(sphere)
        self.components = [sphere]

