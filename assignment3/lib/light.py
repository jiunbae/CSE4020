from OpenGL.GL import *
from OpenGL.GLU import *

from .mode import Mode

class Light:
    class COLOR:
        def __init__(self,
                    ambient = (0,0,0,0),
                    diffuse = (0,0,0,0),
                    specular= (0,0,0,0)):
            self.ambient = ambient
            self.diffuse = diffuse
            self.specular = specular
    index = Mode([GL_LIGHT0, 
                  GL_LIGHT1,
                  GL_LIGHT2,
                  GL_LIGHT3,
                  GL_LIGHT4,
                  GL_LIGHT5,
                  GL_LIGHT6,
                  GL_LIGHT7])
    lights = list()
    obj = COLOR((1., 1., 1., 1.),
                (1., 1., 1., 1.),
                (1., 1., 1., 1.))

    def __init__(self, args):
        self.index = Light.index.get(next=True)
        self.pos = args['pos']
        self.light = Light.COLOR(args['ambient'],
                                 args['diffuse'],
                                 args['specular'])
        Light.lights.append(self)

    def _render(self):
        glEnable(self.index)
        glLightfv(self.index, GL_POSITION, self.pos)
        glLightfv(self.index, GL_AMBIENT, self.light.ambient)
        glLightfv(self.index, GL_DIFFUSE, self.light.diffuse)
        glLightfv(self.index, GL_SPECULAR, self.light.specular)

    @staticmethod
    def objectColor(ambient =(1., 1., 1., 1.),
                    diffuse =(1., 1., 1., 1.),
                    specular=(1., 1., 1., 1.)):
        Light.obj = Light.COLOR(ambient, diffuse, specular)

    @staticmethod
    def render():
        glEnable(GL_LIGHTING)

        for light in Light.lights:
            light._render()

        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, Light.obj.diffuse)

