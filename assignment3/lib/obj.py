import ctypes
from os import path
from itertools import chain

import numpy as np
from numpy import apply_along_axis as npa
from OpenGL.GL import *
from OpenGL.GLU import *

class OBJ:
    _buffer = type('buffer', (), {
        'vertex'    : np.empty((0, 3), dtype=np.float32),
        'normal'    : np.empty((0, 3), dtype=np.float32),
        'texcoord'  : np.empty((0, 3), dtype=np.float32),
    })

    def __init__(self, filename=''):
        self.filename   = filename
        self.array      = None
        self.index      = None
        self.indexes    = dict()
        self.faces      = list()
        self.values     = OBJ._buffer()
        self.buffer     = OBJ._buffer()
        self.face_info  = [0] * 3

    def __str__(self):
        return 'Object Information\n' +\
               ('from file: {}\n'.format(self.filename) if self.filename else '') +\
               '\tTotal number of faces: {}\n'.format(len(self.faces)) +\
               '\tNumber of faces with 3 vertices: {}\n'.format(0) +\
               '\tNumber of faces with 4 vertices: {}\n'.format(0) +\
               '\tNumber of faces with more than 4 vertices: {}\n'.format(0)

    def render(self) -> None:
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        size = self.array.itemsize
        glNormalPointer(GL_FLOAT, 6*size, self.array)
        glVertexPointer(3, GL_FLOAT, 6*size, ctypes.c_void_p(self.array.ctypes.data+3*size))
        glDrawArrays(GL_TRIANGLES, 0, int(self.array.size / 6))

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    @staticmethod
    def trianglize(polygon: np.ndarray) -> np.ndarray:
        count = np.size(polygon, 0)
        triangles = list()

        if sum((polygon[(i + 1)%count][0]-p[0])*(polygon[(i+1)%count][1]+p[1]) for i, p in enumerate(polygon)) > 0:
            polygon = np.flip(polygon, 0)

        _sum = lambda p, q, r: p[0]*(r[1]-q[1]) + q[0]*(p[1]-r[1]) + r[0]*(q[1]-p[1])
        _area = lambda p, q, r: np.abs(_sum(p, q, r) / 2.)
        _inside = lambda v, p, q, r: _area(p, q, r) == sum(_area(p,q,r) for p,q,r in [(v, q, r), (v, p, r), (v, p, q)])
        _ear = lambda p, q, r, polygon: _contain(p,q,r,polygon) and _sum(p, q, r)<0 and _area(p,q,r)

        def _contain(p, q, r, polygon):
            for poly in polygon:
                if tuple(poly) in map(tuple, (p, q, r)): continue
                elif _inside(poly, p, q, r): return False
            return True

        vertex = [tuple(point) for i, point in enumerate(polygon) \
                    if _ear(polygon[i-1], point, polygon[(i+1)%count], polygon)]

        while vertex and count >= 3:
            ear = vertex.pop(0)
            i = np.where(polygon == ear)[0][1]
            prev = polygon[i-1]
            next = polygon[(i+1)%count]
            polygon = np.delete(polygon, i, axis=0)
            count -= 1
            triangles.append((prev, ear, next))
            if count > 3:
                for p, q, r in [(polygon[i-2],prev,next),(prev,next,polygon[(i+2)%count])]:
                    point = tuple(q)
                    if _ear(p, q, r, polygon):
                        if point not in vertex:
                            vertex.append(point)
                    elif point in vertex:
                        vertex.remove(p)
        return np.array(triangles)

    @staticmethod
    def read_obj(filename: str) -> object:
        obj = OBJ(path.basename(filename))

        def _type(v):
            try: return int(v or 0)
            except ValueError:
                return float(v)

        def _update(tar, val):
            if len(val) != np.size(getattr(obj.values, tar), 1):
                setattr(obj.values, tar, np.empty((0, len(val)), dtype=np.float32))
            setattr(obj.values, tar, np.append(getattr(obj.values, tar), [val], axis=0))

        def _match(tar, ary):
            return np.where(npa(lambda x: np.allclose(x, tar), 1, ary) == True)[0][0]

        parse = lambda t, *v: {
            'v' : lambda v: _update('vertex', tuple(map(_type, v))),
            'vn': lambda v: _update('normal', tuple(map(_type, v))),
            'vt': lambda v: _update('texcoord', tuple(map(_type, v))),
            'f' : lambda v: obj.faces.append([tuple(map(_type, z.split('/'))) for z in v]),
        }.get(t,  lambda v: None)(v)

        with open(filename) as file:
            # for line in filter(None, map(str.split, file)):
            #     if line[0] == 'vt':
            #         print (line)
            #     parse(*line)

            any(parse(*line) for line in filter(None, map(str.split, file)))

        newface = list()
        for i, face in enumerate(obj.faces):
            if len(face) > 3:
                normal = face[-1][-1]
                mapping = npa(lambda x: obj.values.vertex[x-1], 1, np.array([face])[:,:,0].T).squeeze()
                f = np.vectorize(lambda x: not np.any(mapping[:,x]-mapping[:,x][0]))
                index = (np.where(f(np.arange(3)) == True)[0] or [0])[0]
                plane = np.delete(mapping, index, 1)
                for triangle in OBJ.trianglize(plane):
                    points = list()
                    for point in triangle:
                        point = np.hstack([point[:index],
                                           mapping[:,index][_match(point, plane)],
                                           point[index:]])
                        try:
                            vi = _match(point, obj.values.vertex)
                        except IndexError:
                            obj.values.vertex = np.vstack([obj.values.vertex, point])
                            vi = np.size(obj.values.vertex, 0)
                        finally:
                            points.append(vi+1)
                    newface.append([(p, 0, normal) for p in points])
            else:
                newface.append(face)

        obj.faces = np.asarray(newface)
        obj.buffer.vertex   = npa(obj.values.vertex.__getitem__, 0, obj.faces[:, :, 0].flatten()-1) if obj.values.vertex.size else None
        obj.buffer.normal   = npa(obj.values.normal.__getitem__, 0, obj.faces[:, 0, 2]-1) if obj.values.normal.size else None
        obj.buffer.texcoord = npa(obj.values.texcoord.__getitem__, 0, obj.faces[:, 0, 0]-1) if obj.values.texcoord.size else None

        w, h = obj.buffer.vertex.shape
        arange = np.arange(w).reshape(w, 1)
        ovn = npa(lambda x: np.stack((x,x,x)), 1, obj.buffer.normal).reshape(w, h)
        obj.array = npa(lambda x: np.stack((ovn[x], obj.buffer.vertex[x])), 1, arange).reshape(w*2, h).astype(np.float32)

        return obj
