import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from .obj import OBJ

class Window:
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name
        self.context = glfw.create_window(width, height, name, None, None)

    def frame(self):
        glBegin(GL_LINES)
        glColor3ub(255,0,0)
        glVertex3fv([0.,0.,0.])
        glVertex3fv([1.,0.,0.])
        glColor3ub(0,255,0)
        glVertex3fv([0.,0.,0.])
        glVertex3fv([0.,1.,0.])
        glColor3ub(0,0,255)
        glVertex3fv([0.,0.,0])
        glVertex3fv([0.,0.,1.])
        glEnd()

    def _callback_key(self, window, key, scancode, action, mods):
        pass

    def _callback_drop(self, window, paths):
        pass

    def render(self):
        pass

