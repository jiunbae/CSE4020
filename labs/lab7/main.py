import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

T = np.identity(4)
rad = 0

def key_callback(window, key, scancode, action, mods):
    global T, rad
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == 49:
            rad -= np.radians(10)
        elif key == 51:
            rad += np.radians(10)
        elif key == 81:
            T = T @ np.array([[1.,0.,0.,-.1], 
                              [0.,1.,0.,0.], 
                              [0.,0.,1.,0.],
                              [0.,0.,0.,1.]])
        elif key == 69:
            T = T @ np.array([[1.,0.,0.,.1], 
                              [0.,1.,0.,0.], 
                              [0.,0.,1.,0.],
                              [0.,0.,0.,1.]])
        elif key == 65:
            T = T @ np.array([[np.cos(np.radians(-10)), 0., np.sin(np.radians(-10)), 0.],
                              [0., 1., 0., 0.], 
                              [-np.sin(np.radians(-10)), 0., np.cos(np.radians(-10)), 0.], 
                              [0.,0.,0.,1.]])
        elif key == 68:
            T = T @ np.array([[np.cos(np.radians(10)), 0., np.sin(np.radians(10)),0.],
                              [0., 1., 0., 0.], 
                              [-np.sin(np.radians(10)), 0., np.cos(np.radians(10)), 0.], 
                              [0.,0.,0.,1.]])
        elif key == 87:
            T = T @ np.array([[1.,0.,0.,0.],
                              [0., np.cos(np.radians(-10)), -np.sin(np.radians(-10)),0.], 
                              [0., np.sin(np.radians(-10)), np.cos(np.radians(-10)),0.], 
                              [0.,0.,0.,1.]])
        elif key == 83:
            T = T @ np.array([[1.,0.,0.,0.],
                              [0., np.cos(np.radians(10)), -np.sin(np.radians(10)),0.], 
                              [0., np.sin(np.radians(10)), np.cos(np.radians(10)),0.], 
                              [0.,0.,0.,1.]])

def clear():
    global rad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    glOrtho(-1,1, -1,1, -1,1)

    gluLookAt(.1*np.sin(rad),.1,.1*np.cos(rad), 0,0,0, 0,1,0)

def axis():
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
    global T
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv((T @ np.array([.0,.5,0.,1.]))[:-1])
    glVertex3fv((T @ np.array([.0,.0,0.,1.]))[:-1])
    glVertex3fv((T @ np.array([.5,.0,0.,1.]))[:-1])
    glEnd()

def main():
    if not glfw.init(): return
    window = glfw.create_window(480, 480, "2015004584", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        clear()
        axis()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()