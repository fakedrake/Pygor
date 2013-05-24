import os
import logging
import logging.config
import argparse
from sys import argv

from pygor.procedure import Procedure
from pygor.emailer import Emailer
from pygor.bigmachine import BigMachine
from pygor.tagger import Tagger
from pygor.settings import (LOGGER_ID, LOG_LEVEL, ENABLE_EMAIL,
                            LOG_FORMAT, SMTP_CONFIG, PYGOR_HELP)

class ContextFilter(logging.Filter):
    """ A fiulter to add some contextual info.
    """

    def filter(self, record):
        if not hasattr(record, 'class_name'):
            record.class_name = LOGGER_ID

        return True



class Pygor(object):
    """ Pygor orichestrates the machinery.
    """

    def __init__(self, properties, log_level=LOG_LEVEL):
        """
	"""
        self.make_directives = open(make_directives_file).readlines()
        self.watched_repos = open(watched_projects_file).readlines()
        self.spamtargets = open(spamtargets_file).readlines()
        self.setup_procedures = open(setup_procedures_file).readlines()

        # Setup the logger
        self.logfile = logfile
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter(LOG_FORMAT)

        hdlr.setFormatter(formatter)
        hdlr.addFilter(ContextFilter())

        self.logger = logging.getLogger(LOGGER_ID)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(log_level)

        self.machine = BigMachine(procedures=map(Procedure, self.setup_procedures), working_dir=working_directory)


    def run(self, enable_email=ENABLE_EMAIL):
        """Add all the tests to the machine, email me the result and if
        everything went well tag the interesting repos.

        """
        for md in self.make_directives:
            self.machine.add_test(md)

        self.machine.run()

        if enable_email:
            emailer = Emailer(self.spamtargets, self.machine)
            emailer.send_email(SMTP_CONFIG, logfile=self.logfile)

        if not self.machine.get_error():
            tagger = Tagger(self.watched_repos)

            tagger.make_tags()
            tagger.flush()


def main():
    parser = argparse.ArgumentParser(description=PYGOR_HELP)
    parser.add_argument('makes', nargs="?", help="Make directives.")
    parser.add_argument('setup', nargs="?", help="Setup commands. Note that the context is lost from one to another. This is not a script")
    parser.add_argument('spamtargets', nargs="?", help="Newline separated email list to send to.")
    parser.add_argument('watched', nargs="?", help="Watched projects list.")
    parser.add_argument('logs', nargs="?", help="Log file.")
    parser.add_argument('cwd', nargs="?", help="The working directory. Note that this is the outer dir(~/Nemas/ eg).")

    args = parser.parse_args(argv[1:])

    servant = Pygor(setup_procedures_file=os.path.abspath(args.setup),
                             make_directives_file=os.path.abspath(args.makes),
                             watched_projects_file=os.path.abspath(args.watched),
                             spamtargets_file=os.path.abspath(args.spamtargets),
                             logfile=os.path.abspath(args.logfile), working_directory=os.path.abspath(args.cwd))
