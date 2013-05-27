import unittest
import logging

from pygor.test.common import in_resources

from pygor.main import Pygor

CONF_FILE = in_resources("props.yaml")
LOG_LEVEL = logging.DEBUG

class TestPygor(unittest.TestCase):
    def setUp(self):
        self.servant = Pygor(CONF_FILE, log_level=LOG_LEVEL)
        self.settings = self.servant.settings
        self.servant.run()


    def test_logging(self):
        logs = open(self.settings["LOGFILE"]).read()
        self.assertIn("Procedure", logs)
        self.assertIn("Emailer", logs)
        self.assertIn("Tagger", logs)
        self.assertIn("MakeProcedure", logs)
