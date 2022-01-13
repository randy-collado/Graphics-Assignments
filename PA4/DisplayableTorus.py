"""
Define Torus here.
First version in 11/01/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from typing import List

from numpy.core.numeric import indices
from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
from Point import Point
import numpy as np
import ColorType
import math
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableTorus(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=1.5, outerRadius=0.5, nsides=100, rings=100, color=ColorType.SOFTBLUE):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.nsides = nsides
        self.rings = rings
        self.color = color

        self.generate(self.innerRadius, self.outerRadius, self.nsides, self.rings, self.color)

    

    def generate(self, innerRadius, outerRadius, nsides, rings, color):
        
        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        self.vertices = np.zeros([(nsides+1) * (rings+1), 11])
        vertices = []
        indices = []
        count = 0
        d_theta = (2*np.pi)/rings
        d_phi = (2*np.pi)/nsides
        theta = 0
        numRings = nsides
        for sides in range(nsides+1):
            phi = -np.pi
            for ring in range(rings+1):
                circle_cross_section = (outerRadius*np.cos(theta)) + innerRadius
                n1, n2, n3 = calculateTorusNorms(theta=theta, phi=phi)
                vertices += [circle_cross_section*np.cos(phi), circle_cross_section*np.sin(phi), outerRadius*np.sin(theta), n1, n2, n3, *color]

                start = (sides * numRings) + ring
                indices += [start, start+numRings+1, start+numRings, start+numRings+1, start, start+1]
                count+=1
                phi += d_phi
            theta += d_theta

        vl = np.array(vertices).reshape(count, 9)
        self.vertices[0:count, 0:9] = vl

        self.indices = np.array(indices)

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)

        self.vao.unbind()

   
def calculateTorusNorms(theta, phi) -> List[float]:
        pass
        delphi_x = -np.sin(phi)
        delphi_y = np.cos(phi)
        delphi_z = 0

        deltheta_x = np.cos(phi)*-np.sin(theta)
        deltheta_y = np.sin(phi)*-np.sin(theta)
        deltheta_z = np.cos(theta)

        nx = delphi_y*deltheta_z - delphi_z*deltheta_y
        ny = delphi_z*deltheta_x - delphi_x*deltheta_z
        nz = delphi_x*deltheta_y - delphi_y*deltheta_x
        return [nx, ny, nz]