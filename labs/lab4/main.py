import glfw
from OpenGL.GL import *
import numpy as np

primitive = 0
def key_callback(window, key, scancode, action, mods):
    global primitive
    if action == glfw.PRESS:
        if key > 47 and key < 58:
            primitive = {   
                1: GL_POINTS,
                2: GL_LINES,
                3: GL_LINE_STRIP,
                4: GL_LINE_LOOP,
                5: GL_TRIANGLES,
                6: GL_TRIANGLE_STRIP,
                7: GL_TRIANGLE_FAN,
                8: GL_QUADS,
                9: GL_QUAD_STRIP,
                0: GL_POLYGON,
            }[key - 48]

def render():
    global primitive
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(primitive)
    glColor3ub(255, 255, 255)

    side = 12
    step = 2 * np.pi / side
    for rad in np.arange(-np.pi, np.pi, step):
        x = np.sin(rad)
        y = np.cos(rad)
        glVertex2fv((x, y))
    glEnd()

def main():
    if not glfw.init(): return
    window = glfw.create_window(480, 480, "Hello World", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()