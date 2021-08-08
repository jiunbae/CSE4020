# -*- coding: utf-8 -*-
""" tests.obj
    ---------------
    Test of OBJ
    :author: jiunbae(jiunbae.623@gmail.com)
"""

import pytest
from lib.obj import OBJ

def test_objload() :
    """ Testing for load obj file
    """

    obj = OBJ.read_obj('./obj/cube-tri.obj')

    assert all(isinstance(it, tuple) for it in obj._vertices)
    assert all(isinstance(it, tuple) for it in obj._normals)
    assert all(isinstance(it, tuple) for it in obj._texcoords)
    assert all(isinstance(it, tuple) for it in obj._faces)
