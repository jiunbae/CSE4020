import glfw
from OpenGL.GL import *
import numpy as np

from collections import OrderedDict

points = OrderedDict([
    ('p0', np.array([200.,200.])),
    ('p1', np.array([300.,350.])),
    ('p2', np.array([500., 550.])),
    ('p3', np.array([400., 400.])),
])
gEditingPoint = ''

def bezier(p0, p1, p2, p3):
    return np.array([[2,-2,1,1],
                     [-3,3,-2,-1],
                     [0,0,1,0],
                     [1,0,0,0]]) @ np.array([[1,0,0,0],
                                             [0,0,0,1],
                                             [-3,3,0,0],
                                             [0,0,-3,3]]) @ np.array([p0, p1, p2, p3])

def render():
    global points
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,640, 0,640, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glBegin(GL_LINE_STRIP)

    glColor3ub(255, 255, 255)
    v = bezier(*points.values())
    for t in np.arange(0, 1.01, .01):
        p = np.array([t**3, t**2, t**1, t**0]) @ v
        glVertex2fv(p)
    glEnd()
    glColor3ub(0,255,0)
    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,.01):
        p = (1-t) * points['p1'] + t * points['p0']
        glVertex2fv(p)
    glEnd()

    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,.01):
        p = (1-t) * points['p2'] + t*points['p3']
        glVertex2fv(p)
    glEnd()

    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,.01):
        p = (1-t) * points['p2'] + t*points['p1']
        glVertex2fv(p)
    glEnd()

    glBegin(GL_LINE_STRIP)
    for t in np.arange(0,1,.01):
        p = (1-t) * points['p0'] + t*points['p3']
        glVertex2fv(p)
    glEnd()
    glPointSize(20.)
    glColor3ub(0,255,0)
    glBegin(GL_POINTS)
    glVertex2fv(points['p0'])
    glVertex2fv(points['p1'])
    glVertex2fv(points['p2'])
    glVertex2fv(points['p3'])
    glEnd()

def button_callback(window, button, action, mod):
    global points, gEditingPoint
    if button==glfw.MOUSE_BUTTON_LEFT:
        x, y = glfw.get_cursor_pos(window)
        y = 640 - y
        if action==glfw.PRESS:
            for k, p in points.items():
                if np.abs(x-p[0])<10 and np.abs(y-p[1])<10:
                    gEditingPoint = k
        elif action==glfw.RELEASE:
            gEditingPoint = ''

def cursor_callback(window, xpos, ypos):
    global points, gEditingPoint
    ypos = 640 - ypos
    if gEditingPoint:
        points[gEditingPoint][0] = xpos
        points[gEditingPoint][1] = ypos

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2015004584', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

