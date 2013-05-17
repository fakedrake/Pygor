import os
import unittest

from pygor.test.common import in_resources
from pygor.procedure import MakeProcedure, Procedure

MAKEFILE_DIR = in_resources("")

class TestMakeProcedure(unittest.TestCase):

    def test_make(self):
        proc = MakeProcedure("hello_world", working_dir=MAKEFILE_DIR)

        proc.run()
        self.assertEquals(proc.stdout, "Hello world!\n")

    def test_general(self):
        p = Procedure("echo 'Hello world'")

        p.run()
        self.assertEquals(p.stdout, "Hello world\n")
