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


class TestMakeProcedure(unittest.TestCase):

    def test_output(self):
        p = Procedure("echo 'Hello world'")

        p.run()
        self.assertEquals(p.get_output(), "Hello world\n")

    def test_success(self):
        p = Procedure("echo 'Hello world'")

        p.run()
        self.assertEquals(p.get_output(), "Hello world\n")
        self.assertEquals(p.get_title(), "echo 'Hello world'")
        self.assertEquals(p.get_exit(), 0)
        self.assertEquals(p.get_error(), None)

    def test_fail(self):
        p = Procedure("bash -i -c \"echo 'Hello world'>&2 && exit 1\"")

        p.run()

        self.assertIn("world", p.get_error())
