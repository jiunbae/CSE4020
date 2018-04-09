import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
gCamAng = 0.
gCamHeight = 1.

def myOrtho(l, r, b, t, n, f):
   glMultMatrixf(
      np.array([
         [2/(r-l), 0, 0, -(r+l)/(r-l)],
         [0, 2/(t-b), 0, -(t+b)/(t-b)],
         [0, 0, -2/(f-n), -(f+n)/(f-n)],
         [0, 0, 0, 1]
      ]).T
   )

# draw a cube of side 1, centered at the origin.
def drawUnitCube():
   glBegin(GL_QUADS)
   glVertex3f( 0.5, 0.5,-0.5)
   glVertex3f(-0.5, 0.5,-0.5)
   glVertex3f(-0.5, 0.5, 0.5)
   glVertex3f( 0.5, 0.5, 0.5)
   glVertex3f( 0.5,-0.5, 0.5)
   glVertex3f(-0.5,-0.5, 0.5)
   glVertex3f(-0.5,-0.5,-0.5)
   glVertex3f( 0.5,-0.5,-0.5)
   glVertex3f( 0.5, 0.5, 0.5)
   glVertex3f(-0.5, 0.5, 0.5)
   glVertex3f(-0.5,-0.5, 0.5)
   glVertex3f( 0.5,-0.5, 0.5)
   glVertex3f( 0.5,-0.5,-0.5)
   glVertex3f(-0.5,-0.5,-0.5)
   glVertex3f(-0.5, 0.5,-0.5)
   glVertex3f( 0.5, 0.5,-0.5)
   glVertex3f(-0.5, 0.5, 0.5)
   glVertex3f(-0.5, 0.5,-0.5)
   glVertex3f(-0.5,-0.5,-0.5)
   glVertex3f(-0.5,-0.5, 0.5)
   glVertex3f( 0.5, 0.5,-0.5)
   glVertex3f( 0.5, 0.5, 0.5)
   glVertex3f( 0.5,-0.5, 0.5)
   glVertex3f( 0.5,-0.5,-0.5)
   glEnd()

def drawCubeArray():
   for i in range(5):
      for j in range(5):
         for k in range(5):
            glPushMatrix()
            glTranslatef(i,j,-k-1)
            glScalef(.5,.5,.5)
            drawUnitCube()
            glPopMatrix()

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
   glPolygonMode(GL_FRONT_AND_BACK, GL_LINE )
 
   glLoadIdentity()
   myOrtho(-5, 5, -5, 5, -10, 10)

   gluLookAt(1*np.sin(gCamAng),gCamHeight,1*np.cos(gCamAng), 0,0,0, 0,1,0)
   drawFrame()
   glColor3ub(255, 255, 255)
   drawCubeArray()

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

def main():
   if not glfw.init():
      return
   window = glfw.create_window(640,640,'2015004584', None,None)
   if not window:
      glfw.terminate()
      return
   glfw.make_context_current(window)
   glfw.set_key_callback(window, key_callback)
   
   while not glfw.window_should_close(window):
      glfw.poll_events()
      render()
      glfw.swap_buffers(window)
   
   glfw.terminate()

if __name__ == "__main__":
   main()