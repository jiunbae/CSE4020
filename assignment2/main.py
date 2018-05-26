import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

from math import factorial

gCamAng = 0.
gCamHeight = 1.
counter = 0

def bezier(points, detail=128):
    def bpoly(i, n, t):
        comb = lambda n, k: factorial(n) / factorial(k) / factorial(n - k)
        return comb(n, i) * (t**(n-i)) * (1 - t)**i

    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, detail)
    parray = np.array([bpoly(i, len(points)-1, t) for i, _ in enumerate(points)])

    return np.dot(xPoints, parray), np.dot(yPoints, parray)

def drawText(xoff, yoff, z):
    glColor3ub(255, 255, 255)
    glPushMatrix()
    for c, vertex in [('H', [(197,284),(218,291),(199,416),(180,454),(273,422),(254,410),(260,356),(316,350),(312,394),(294,418),(333,411),(363,380),(371,293),(348,274),(387,257),(308,272),(323,282),(320,318),(263,332),(270,282),(288,261)]),
                      ('E', [(362,277),(382,293),(376,382),(351,406),(466,392),(524,401),(485,354),(471,364),(425,367),(426,341),(457,336),(481,344),(459,308),(429,315),(429,293),(466,288),(484,296),(486,262)]),
                      ('R', [(493,260),(491,347),(522,386),(562,384),(543,372),(542,351),(591,381),(656,381),(591,344),(613,322),(620,256)]),
                      ('O', []),
                      ('E', [(804,258),(819,271),(819,367),(783,390),(904,403),(950,356),(914,370),(876,365),(875,338),(903,340),(928,350),(909,312),(900,317),(872,313),(870,291),(905,294),(913,303),(946,276)]),
                      ('S', [(990,256),(933,302),(1044,391),(967,376),(957,361),(904,421),(965,415),(1109,454),(1095,387),(1067,353),(986,298),(1000,285),(1025,292),(1031,314),(1071,273)])]:
        glBegin(GL_POLYGON)
        for x, y in vertex:
            glVertex3f((x-620)/1080+xoff, -(y-300)/1080+yoff, z)
        glEnd()
    glPopMatrix()

def drawWing(detail=32):
    def _draw(inner, outer, z, detail=32):
        glBegin(GL_POLYGON)
        for x, y in zip(*bezier(inner, detail)):
            glVertex3f(x, y, z)
        xs, ys = bezier(outer, detail)
        for x, y in zip(reversed(xs), reversed(ys)):
            glVertex3f(x, y, z)
        glEnd()

    _draw(np.array([(0, 0), (20, -5), (50, 10), (60, 50)])/100,
            np.array([(0, 0), (30, -15), (65, -5), (80, 30)])/100, .0, detail)

    glPushMatrix()
    _draw(np.array([(10, -2), (20, -5), (55, 10), (61, 45)])/100,
            np.array([(10, -2), (25, -10), (60, -5), (76, 30)])/100, .1, detail)
    glPopMatrix()

def drawHexagon(z):
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex3f(np.sin(i/6.*2*np.pi), np.cos(i/6.*2*np.pi), z)
    glEnd();

def drawHOS(detail=32):
    global counter

    glColor3ub(0, 121, 255)
    glPushMatrix()
    drawHexagon(-.1)

    glColor3ub(141, 213, 255)
    glScalef(1.3,1.3,1.3)
    glPushMatrix()
    for i in range(3):
        glPushMatrix()
        glRotatef((counter + i * 120) % 360, 0, 0, 1)
        glTranslatef(-.275, -.45, 0)
        drawWing(detail)
        glPopMatrix()

    glPopMatrix()

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
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLoadIdentity()
    gluPerspective(25, 1, 1, 10)
    gluLookAt(5*np.sin(gCamAng), gCamHeight, 5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()
    glScalef(2.4,2.4,2.4)
    drawText(.0, .0, -.05)
    glTranslatef(.09, -.025, .0)

    if counter < 500:
        glScalef(15/((counter+1)/5),15/((counter+1)/5),15/((counter+1)/5))
    else:
        glScalef(15/100,15/100,15/100)

    drawHOS()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, counter
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_A:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_D:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_W:
            gCamHeight += .1
        elif key==glfw.KEY_S:
            gCamHeight += -.1
        elif key==glfw.KEY_R:
            counter = 0

def main():
    global counter
    if not glfw.init(): return

    window = glfw.create_window(640, 640, '2015004584', None, None)
    if not window:
        glfw.terminate()
        return
   
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        counter += 1
        glfw.swap_buffers(window)

        if counter > 36000:
            counter = 0

    glfw.terminate()

if __name__ == "__main__":
    main()
