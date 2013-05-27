import os
import unittest
import logging

from pygor.logger import Logger
from pygor.settings import LOGGER_ID
from pygor.test.common import in_resources


LOG_FILE = in_resources("logger")

class ClassA(Logger):
    def foo(self):
        pass


class TestMakeProcedure(unittest.TestCase):

    def setUp(self):
        self.main_logger = logging.getLogger(LOGGER_ID)
        fh = logging.FileHandler(LOG_FILE, "w")
        formatter = logging.Formatter("%(class_name)s: %(message)s")
        fh.setFormatter(formatter)
        self.main_logger.addHandler(fh)
        self.a = ClassA()

    def test_error(self):
        self.a.logger.error("here is an error")
        self.assertIn("ClassA", open(LOG_FILE).read())

    def test_functionlog(self):
        self.main_logger.setLevel(logging.DEBUG)
        self.a.foo()
        self.assertIn("foo", open(LOG_FILE).read())

    def tearDown(self):
        open(LOG_FILE, "w").write("")
