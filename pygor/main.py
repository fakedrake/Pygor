import logging

from pygor.emailer import Emailer
from pygor.BigMachine import BigMachine
from pygor.tagger import Tagger
from pygor.settings import LOGGER_ID, LOG_LEVEL

class Pygor(object):
    """ Pygor orichestrates the machinery.
    """

    def __init__(self, make_directives_file, watched_projects_file, spamtargets_file, logfile):
        """
	"""
        self.make_directives = make_directives_file.readlines()
        self.watched_repos = watched_projects_file.readlines()
        self.spamtargets = spamtargets_file.readlines()

        # Setup the logger
        self.logger = logging.getLogger(LOGGER_ID)
        self.logger.fileConfig(logfile)
        self.logger.setLevel(LOG_LEVEL)

        self.machine = BigMachine()


    def check_tree(self, enable_email=ENABLE_EMAIL):
        """Add all the tests to the machine, email me the result and if
        everything went well tag the interesting repos.

        """
        for md in self.make_directives:
            self.machine.add_test(md)

        self.machine.run()

        if enable_email:
            emailer = Emailer(self.spamtargets, machine)
            emailer.send_email(self.logfile)

        if not machine.get_error():
            tagger = Tagger(self.watched_repos)

            tagger.make_tags()
            tagger.flush()
