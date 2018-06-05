import glfw
from OpenGL.GL import *
import numpy as np

from collections import OrderedDict

points = OrderedDict([
    ('p0', np.array([200.,200.])),
    ('p1', np.array([400.,400.])),
    ('pv0', np.array([300., 350.])),
    ('pv1', np.array([500., 550.])),
])
gEditingPoint = ''

def hermit(p0, p1, pv0, pv1):
    v0 = pv0 - p0
    v1 = pv1 - p1
    return np.array([[ 2,-2, 1, 1],
                     [-3, 3,-2,-1],
                     [ 0, 0, 1, 0],
                     [ 1, 0, 0, 0]]) @ np.array([p0, p1, v0, v1])

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
    glColor3ub(0, 255, 0)
    for t in np.arange(0, 1.01, .01):
        p = (1-t)*points['pv0'] + t*points['p0']
        glVertex2fv(p)
    glColor3ub(255, 255, 255)

    v = hermit(*points.values())
    for t in np.arange(0, 1.01, .01):
        p = np.array([t**3, t**2, t**1, t**0]) @ v
        glVertex2fv(p)
    glColor3ub(0, 255, 0)
    for t in np.arange(0, 1.01, .01):
        p = (1-t)*points['pv1'] + t*points['p1']
        glVertex2fv(p)
    glEnd()

    glColor3ub(255, 255, 255)
    glPointSize(20.)
    glBegin(GL_POINTS)
    for p in points.values():
        glVertex2fv(p)
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

