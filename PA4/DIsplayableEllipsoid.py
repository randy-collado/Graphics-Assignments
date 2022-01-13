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

class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    slices = 0
    stacks = 0
    xRadius = 0
    yRadius = 0
    zRadius = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, xRadius=0.5, yRadius=0.5, zRadius=0.5, slices=45, stacks=45, color=ColorType.SOFTBLUE):
        super(DisplayableEllipsoid, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(xRadius, yRadius, zRadius, slices, stacks, color)

    def generate(self, xRadius, yRadius, zRadius, slices, stacks, color=ColorType.SOFTBLUE):
        self.xRadius = xRadius
        self.yRadius = yRadius
        self.zRadius = zRadius
        self.slices = slices
        self.stacks = stacks
        self.color = color

        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        self.vertices = np.zeros([(slices+1) * (stacks+1), 11])
        vertices = []
        indices = []
        count = 0
        d_theta = (2*np.pi)/slices
        d_phi = np.pi/stacks
        theta = -np.pi
        numSlices = slices
        for slic in range(0, slices+1):
            phi = -np.pi/2
            for stack in range(0, stacks+1):
                x = np.cos(theta)*np.cos(phi)
                y = np.sin(theta)*np.cos(phi)
                z = np.sin(phi)
                vertices += [xRadius*x, yRadius*y, zRadius*z, x, y, z, *color]
                phi += d_phi
                count+=1

                #ellipsoid indices from https://stackoverflow.com/questions/60686457/issue-in-drawing-ellipsoid-with-opengl

                start = (slic * numSlices) + stack
                indices += [start, start+numSlices+1, start+numSlices, start+numSlices+1, start, start+1]
            theta += d_theta

        vl = np.array(vertices).reshape((count, 9))
        self.vertices[0:count, 0:9] = vl

        self.indices = np.array(indices, dtype="int32")

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