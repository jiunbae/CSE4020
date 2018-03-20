import glfw
from OpenGL.GL import *
import numpy as np

T = [[1, 0],
     [0, 1]]

def key_callback(window, key, scancode, action, mods):
    global T
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == 87:
            T = np.array([[.9, 0],
                          [0, 1]]) @ T
        elif key == 69:
            T = np.array([[1.1, 0],
                          [0, 1]]) @ T
        elif key == 83:
            T = np.array([[np.cos(np.radians(10)), -np.sin(np.radians(10))],
                          [np.sin(np.radians(10)), np.cos(np.radians(10))]]) @ T
        elif key == 68:
            T = np.array([[np.cos(np.radians(-10)), -np.sin(np.radians(-10))],
                          [np.sin(np.radians(-10)), np.cos(np.radians(-10))]]) @ T
        elif key == 88:
            T = np.array([[1, .1],
                          [0, 1]]) @ T
        elif key == 67:
            T = np.array([[1, -.1],
                          [0, 1]]) @ T
        elif key == 82:
            T = np.array([[1, 0],
                          [0, -1]]) @ T
        elif key == 49:
            T = np.array([[1, 0],
                          [0, 1]])
        else:
            pass

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
   
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(T @ np.array([0.0,0.5]))
    glVertex2fv(T @ np.array([0.0,0.0]))
    glVertex2fv(T @ np.array([0.5,0.0]))
    glEnd()

def main():
    global T
    if not glfw.init(): return
    window = glfw.create_window(480, 480, "Hello World", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(T)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()