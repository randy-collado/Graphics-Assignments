from Component import Component
from Point import Point
import ColorType as Ct
from DisplayableTriPrism import DisplayableTriPrism

class TriPrismComponent(Component):
    """
    Define our Sphere model
    """

    components = None
    contextParent = None
    position = None
    scale = None

    def __init__(self, parent, position, color, scale=[1, 1, 1], display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent
        self.position = position
        self.scale = scale 

        finn: Component = Component(Point((0, 0, 0)), DisplayableTriPrism(self.contextParent, scale=self.scale))
        finn.setDefaultColor(color)
        self.addChild(finn)
        self.components = [finn]

