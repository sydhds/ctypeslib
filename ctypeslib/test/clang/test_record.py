import sys
import os
import unittest
import tempfile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import ctypes
from ctypes.util import find_library
from ctypeslib import clang2py
from ctypeslib.codegen.codegenerator import generate_code

from util import get_cursor
from util import get_tu

class ADict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

class ArchTest(unittest.TestCase):
    word_size = None
    flags = []
    def gen(self, fname, flags=None):
        args = [fname]
        args.extend(self.flags)
        if flags:
            args.extend(flags)
            
        ofi = StringIO()
        #ofi = sys.stdout
        generate_code(args, ofi, use_clang=True) #, **kw)
        namespace = {}
        exec ofi.getvalue() in namespace
        #print ofi.getvalue()
        return ADict(namespace)


class X32Test(ArchTest):
    flags = ['-target','i386-linux']

class X64Test(ArchTest):
    flags = ['-target','x86_64-linux']
    
    
class RecordTestX32(X32Test):
    def test_padding(self):
        self.namespace = self.gen('test/clang/test-clang5.c')
        
        self.assertEquals(ctypes.sizeof(self.namespace.structName), 14)
        self.assertEquals(ctypes.sizeof(self.namespace.structName2), 16)
        self.assertEquals(ctypes.sizeof(self.namespace.Node), 16)
        self.assertEquals(ctypes.sizeof(self.namespace.Node2), 8)
        self.assertEquals(ctypes.sizeof(self.namespace.Node3), 12)
        self.assertEquals(ctypes.sizeof(self.namespace.Node4), 12)
        self.assertEquals(ctypes.sizeof(self.namespace.Node5), 8)
        self.assertEquals(ctypes.sizeof(self.namespace.my_bitfield), 16)

        





if __name__ == "__main__":
    unittest.main()
