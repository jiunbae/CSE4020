import glfw

from .obj import OBJ

class Window:
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name
        self.context = glfw.create_window(width, height, name, None, None)

    def _callback_key(self, window, key, scancode, action, mods):
        pass

    def _callback_drop(self, window, paths):
        pass

    def render(self):
        pass

