from os import path
from collections import OrderedDict
from itertools import chain

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class OBJ:
    _buffer = type('buffer', (), {
        'vertex'    : np.empty((0, 3)),
        'normal'    : np.empty((0, 3)),
        'texcoord'  : np.empty((0, 3)),
    })

    def __init__(self, filename=''):
        self.filename   = filename
        self.index      = None
        self.indexes    = dict()
        self.faces      = list()
        self.values     = OBJ._buffer()
        self.buffer     = OBJ._buffer()

    def __str__(self):
        return 'Object Information\n' +\
               ('from file: {}\n'.format(self.filename) if self.filename else '') +\
               '\tTotal number of faces: {}\n'.format(len(self.faces)) +\
               '\tNumber of faces with 3 vertices: {}\n'.format(0) +\
               '\tNumber of faces with 4 vertices: {}\n'.format(0) +\
               '\tNumber of faces with more than 4 vertices: {}\n'.format(0)

    def render(self):
        glBegin(GL_POLYGON)
        for v, n, t in zip(self.buffer.vertex, self.buffer.normal, self.buffer.texcoord):
            if self.values.normal.size:
                glNormal3fv(n)
            if self.values.texcoord.size :
                glTexCoord2fv(t)
            glVertex3fv(v)
        glEnd()

    @staticmethod
    def read_obj(filename):
        obj = OBJ(path.basename(filename))

        def _type(v):
            try: return int(v or 0)
            except ValueError:
                return float(v)

        def _update(tar, val):
            setattr(obj.values, tar, np.append(getattr(obj.values, tar), [val], axis=0))

        parse = lambda t, *v: {
            'v' : lambda v: _update('vertex', tuple(map(_type, v))),
            'vn': lambda v: _update('normal', tuple(map(_type, v))),
            'vt': lambda v: _update('texcoord', tuple(map(_type, v))),
            'f' : lambda v: obj.faces.append([tuple(map(_type, z.split('/'))) for z in v]),
        }.get(t,  lambda v: None)(v)

        with open(filename) as file:
            any(parse(*line) for line in map(str.split, file))

        # obj.indexes = {f: i for i, f in enumerate(set(chain(*obj.faces)))}
        count = 0
        for index in chain(*obj.faces):
            if index not in obj.indexes:
                obj.indexes[index] = count
                count +=1 

        obj.faces = np.asarray(obj.faces)
        obj.buffer.vertex   = np.empty((len(obj.indexes), 3), np.float32)
        obj.buffer.normal   = np.empty((len(obj.indexes), 3), np.float32)
        obj.buffer.texcoord = np.empty((len(obj.indexes), 2), np.float32)

        for index, value in obj.indexes.items():
            obj.buffer.vertex[value]   = obj.values.vertex[index[0]-1]   if obj.values.vertex.size else 0
            obj.buffer.normal[value]   = obj.values.normal[index[2]-1]   if obj.values.normal.size else 0
            obj.buffer.texcoord[value] = obj.values.texcoord[index[1]-1] if obj.values.texcoord.size else 0
        obj.index = np.apply_along_axis(lambda x: obj.indexes[tuple(x)], 2, obj.faces)

        return obj
