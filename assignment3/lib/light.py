from OpenGL.GL import *
from OpenGL.GLU import *

from .mode import Mode

class Light:
    index = Mode([GL_LIGHT0, 
                  GL_LIGHT1,
                  GL_LIGHT2,
                  GL_LIGHT3,
                  GL_LIGHT4,
                  GL_LIGHT5,
                  GL_LIGHT6,
                  GL_LIGHT7])

    class COLOR:
        def __init__(self, ambient=(0,0,0,0), diffuse=(0,0,0,0), specular=(0,0,0,0)):
            self.ambient = ambient
            self.diffuse = diffuse
            self.specular = specular

    def __init__(self, args):
        self.index = Light.index.get(next=True)
        print (self.index)
        self.pos = args['pos']
        self.light = Light.COLOR(args['ambient'],args['diffuse'],args['specular'])

    def render(self):
        glPushMatrix()

        glLightfv(self.index, GL_POSITION, self.pos)

        glPopMatrix()

        glLightfv(self.index, GL_AMBIENT, self.light.ambient)
        glLightfv(self.index, GL_DIFFUSE, self.light.diffuse)
        glLightfv(self.index, GL_SPECULAR, self.light.specular)
