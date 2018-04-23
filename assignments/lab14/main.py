import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
gCamAng = 0.
gCamHeight = 1.
glVertexArraySeparate = None

def createUnitCube_glDrawArrays():
   return np.array([
      [.5, .5, -.5],
      [-.5, .5, -.5],
      [-.5, .5, .5],

      [.5, .5, -.5],
      [-.5, .5, .5],
      [.5, .5, .5],

      [.5, -.5, .5],
      [-.5, -.5, .5],
      [-.5, -.5, -.5],

      [.5, -.5, .5],
      [-.5, -.5, -.5],
      [.5, -.5, -.5],

      [.5, .5, .5],
      [-.5, .5, .5],
      [-.5, -.5, .5],

      [.5, .5, .5],
      [-.5, -.5, .5],
      [.5, -.5, .5],

      [.5, -.5, -.5],
      [-.5, -.5, -.5],
      [-.5, .5, -.5],

      [.5, -.5, -.5],
      [-.5, .5, -.5],
      [.5, .5, -.5],

      [-.5, .5, .5],
      [-.5, .5, -.5],
      [-.5, -.5, -.5],

      [-.5, .5, .5],
      [-.5, -.5, -.5],
      [-.5, -.5, .5],

      [.5, .5, -.5],
      [.5, .5, .5],
      [.5, -.5, .5],

      [.5, .5, -.5],
      [.5, -.5, .5],
      [.5, -.5, -.5],
   ], 'float32')

def drawUnitCube_glDrawArrays():
   global glVertexArraySeparate
   varr = glVertexArraySeparate
   glEnableClientState(GL_VERTEX_ARRAY)
   glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
   glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))

def drawFrame():
   glBegin(GL_LINES)
   glColor3ub(255, 0, 0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([1.,0.,0.]))
   glColor3ub(0, 255, 0)
   glVertex3fv(np.array([0.,0.,0.]))
   glVertex3fv(np.array([0.,1.,0.]))
   glColor3ub(0, 0, 255)
   glVertex3fv(np.array([0.,0.,0]))
   glVertex3fv(np.array([0.,0.,1.]))
   glEnd()

def render():
   global gCamAng, gCamHeight
   glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
   glEnable(GL_DEPTH_TEST)
   glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

   glLoadIdentity()
   gluPerspective(45, 1, 1,10)
   gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)
   
   drawFrame() 
   glColor3ub(255, 255, 255)
   drawUnitCube_glDrawArrays()

def key_callback(window, key, scancode, action, mods):
   global gCamAng, gCamHeight
   if action==glfw.PRESS or action==glfw.REPEAT:
      if key==glfw.KEY_1:
         gCamAng += np.radians(-10)
      elif key==glfw.KEY_3:
         gCamAng += np.radians(10)
      elif key==glfw.KEY_2:
         gCamHeight += .1
      elif key==glfw.KEY_W:
         gCamHeight += -.1

def windows_callback(window, width, height):
   glViewport(0, 0, width, height)

def main():
   global glVertexArraySeparate
   if not glfw.init():
      return
   window = glfw.create_window(640,640,'2015004584', None,None)
   if not window:
      glfw.terminate()
      return
   glfw.make_context_current(window)
   glfw.set_key_callback(window, key_callback)
   glfw.set_framebuffer_size_callback(window, windows_callback)

   glVertexArraySeparate = createUnitCube_glDrawArrays()
   while not glfw.window_should_close(window):
      glfw.poll_events()
      render()
      glfw.swap_buffers(window)
   
   glfw.terminate()

if __name__ == "__main__":
   main()