from collections import OrderedDict
from itertools import chain

import numpy as np

class OBJ:
    _buffer = type('buffer', (), {
        'vertex': np.zeros((0, 3)),
        'normal': np.zeros((0, 3)),
        'texcoord': np.zeros((0, 3))
    })

    def __init__(self):
        self._faces = list()
        self.values = OBJ._buffer()
        self.buffer = OBJ._buffer()

    @staticmethod
    def read_obj(filename):
        obj = OBJ()

        def _type(v):
            try:
                return tuple(map(int, v))
            except ValueError:
                return tuple(map(float, v))
        def _update(tar, val):
            setattr(obj.values, tar, np.append(getattr(obj.values, tar), [val], axis=0))

        parse = lambda t, *v: {
            'v' : lambda v: _update('vertex', _type(v)),
            'vn': lambda v: _update('normal', _type(v)),
            'vt': lambda v: _update('texcoord', _type(v)),
            'f' : lambda v: obj._faces.append(tuple(_type(z.split('//')) for z in v)),
        }.get(t, lambda v: None)(v)

        with open(filename) as file:
            any(parse(*line) for line in map(str.split, file))

        indexes = OrderedDict.fromkeys(chain(*obj._faces))

        obj.buffer.vertex = np.ndarray((len(indexes), 3), np.float32)
        obj.buffer.normal = np.ndarray((len(indexes), 3), np.float32)        
        obj.buffer.texcoord = np.ndarray((len(indexes), 3), np.float32)
        for index, value in enumerate(indexes):
            obj.buffer.vertex[index] = obj.values.vertex[value[0]-1]
            obj.buffer.normal[index] = obj.values.normal[value[0]-1]
            obj.buffer.texcoord[index] = obj.values.texcoord[value[0]-1]

        print (obj.buffer.vertex)
        print (obj.buffer.normal)
        print (obj.buffer.texcoord)

        return obj
