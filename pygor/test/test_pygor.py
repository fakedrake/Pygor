import unittest
import logging

from pygor.test.common import in_resources

from pygor.main import Pygor

SETUP = in_resources("setup")
MAKES = in_resources("makes")
WATCHED = in_resources("watched")
SPAMTARGETS = in_resources("spamtargets")
LOGFILE = in_resources("logfile")
CWD = in_resources("BTags")

LOG_LEVEL = logging.DEBUG

class TestPygor(unittest.TestCase):
    def setUp(self):
        self.servant = Pygor(setup_procedures_file=SETUP,
                             make_directives_file=MAKES,
                             watched_projects_file=WATCHED,
                             spamtargets_file=SPAMTARGETS,
                             logfile=LOGFILE, working_directory=CWD,
                             log_level=LOG_LEVEL)

        self.servant.run()


    def test_logging(self):
        logs = open(LOGFILE).read()
        self.assertIn("Procedure", logs)
        self.assertIn("Emailer", logs)
        self.assertIn("Tagger", logs)
        self.assertIn("MakeProcedure", logs)
