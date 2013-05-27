import os
import logging
import logging.config
import argparse
from sys import argv

from pygor.procedure import Procedure
from pygor.emailer import Emailer
from pygor.bigmachine import BigMachine
from pygor.tagger import Tagger
from pygor.settings_manager import Settings, updated_settings


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

    def __init__(self, config_file, **kwargs):
        """
	"""
        self.config = Settings(config_file)
        self.settings = updated_settings(self.config.settings, **kwargs)

        self.make_directives = self.config.make_cmds
        self.watched_repos = self.config.watched_repos
        self.spamtargets = self.config.spamtargets
        self.setup_procedures = self.config.setup_cmds

        # Setup the logger
        self.logfile = self.settings["LOGFILE"]
        hdlr = logging.FileHandler(self.logfile)
        formatter = logging.Formatter(self.settings["LOG_FORMAT"])

        hdlr.setFormatter(formatter)
        hdlr.addFilter(ContextFilter())

        self.logger = logging.getLogger(self.settings["LOGGER_ID"])
        self.logger.addHandler(hdlr)
        self.logger.setLevel(self.settings["LOG_LEVEL"])

        self.machine = BigMachine(procedures=map(Procedure,
                                                 self.setup_procedures),
                                  working_dir=self.settings["WORKING_DIR"])


    def run(self, **kwargs):
        """Add all the tests to the machine, email me the result and if
        everything went well tag the interesting repos.

        """
        settings = updated_settings(self.settings, **kwargs)

        for md in self.make_directives:
            self.machine.add_test(md)

        self.machine.run()

        if settings["ENABLE_EMAIL"]:
            emailer = Emailer(self.machine, self.config)
            emailer.send_email(smtp_config=settings["SMTP_CONFIG"], logfile=self.logfile)

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
