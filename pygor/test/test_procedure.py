import os
import unittest

from pygor.test.common import MAKEFILE_DIR

from pygor import MakeProcedure, Procedure

class TestMakeProcedure(unittest.TestCase):

    def test_make(self):
        proc = MakeProcedure("hello_world", working_dir=MAKEFILE_DIR)

        proc.run()
        self.assertEquals(proc.stdout, "Hello world!\n")

    def test_general(self):
        p = Procedure("echo 'Hello world'")

        p.run()
        self.assertEquals(p.stdout, "Hello world\n")
