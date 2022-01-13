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

class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    slices = 0
    stacks = 0
    radius = 0
    height = 0
    color = None

    vertices = None
    indices = None

    def __init__(self, shaderProg, radius=0.25, height=0.5, slices=36, stacks=36, color=ColorType.SOFTGREEN):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, height, slices, stacks, color)

    def generate(self, radius, height, slices, stacks, color):
        self.radius = radius
        self.height = height
        self.slices = slices
        self.stacks = stacks
        self.color = color

        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        top_vertices, tvLength, top_indices, tIndexLength = self.generateCapsEBO(slices, radius, height, color, is_forward_facing=True) 
        bottom_vertices, bvLength, bottom_indices, bIndexLength = self.generateCapsEBO(slices, radius, height, color, is_forward_facing=False)

        self.vertices = np.zeros([( (slices+1) * (stacks+1) ) + tvLength + bvLength, 11])
        vertices = []
        indices = []
        d_height = height / stacks
        d_theta = (2*np.pi) / slices
        h = -height/2
        count = 0
        numSlices = slices +1


        for stack in range(stacks+1):
            theta = -np.pi
            for slic in range(slices+1):
                cos = np.cos(theta)
                sin = np.sin(theta)
                vertices+=[radius*cos, radius*sin, h, cos, sin, 0, *color]
                theta += d_theta
                count+=1
                #indices from https://stackoverflow.com/questions/60686457/issue-in-drawing-ellipsoid-with-opengl
                currentQuad = (stack * numSlices) + slic
                indices += [currentQuad, currentQuad+numSlices+1, currentQuad+numSlices, currentQuad+numSlices+1, currentQuad, currentQuad+1]
            h += d_height

        vertices += top_vertices + bottom_vertices
        self.shiftVector(top_indices, count)
        self.shiftVector(bottom_indices, tvLength + count)
        vl = np.array(vertices).reshape((count + tvLength + bvLength, 9))
        self.vertices[0:count + tvLength + bvLength, 0:9] = vl

        self.indices = np.array(indices + top_indices + bottom_indices, dtype="int32")
    
    def generateCapsEBO(self, slices, radius, height, color, is_forward_facing):
        theta = -np.pi
        d_theta = (2*np.pi) / slices

        vertices = []
        indices = []
        vertices += [0, 0, (-height/2 if is_forward_facing else height/2), 0, 0, (-1 if is_forward_facing else 1), *color]
        vertices_length = 1
        indices_length = 0
        
        for i in range(slices+1):
            if is_forward_facing:
                vertices += [radius*np.sin(theta), radius*np.cos(theta), -height/2, 0, 0, -1, *color]
            else:
                vertices += [radius*np.sin(theta), radius*np.cos(theta), height/2, 0, 0, 1, *color]
            theta += d_theta
            vertices_length += 1

        for i in range(1, slices+2):
            indices += [0, i, (i+1)]
            indices_length+=1
        return vertices, vertices_length, indices, indices_length

    def shiftVector(self, vec, shift):
        for idx in range(len(vec)):
            vec[idx] += shift



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