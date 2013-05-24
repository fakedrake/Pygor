import os
import shlex
from subprocess import Popen, PIPE

from pygor.logger import Logger
from pygor.settings_manager import DEFAULT_SETTINGS, update_settings

class Procedure(Logger):
    """ Subclass this to create a procedure that the Big Machine can run.
    """

    def __init__(self, command, expected_exit=0, working_dir=None, conf=DEFAULT_SETTINGS, **kwargs):
        """Most of the time creating the right procedure will be just
        enough. The parametrizer is a callable expected to return a
        dict to dynamically format command with a single parameter
        this procedure.

        Extend this to make more specific procedures. A procedure in
        general can only be relied upon to have the following.

        - run
        - get_error
        - get_output
        - get_exit

        """
        self.command = command
        self.expected_exit = expected_exit
        self.working_dir = working_dir

        self.stdout = None
        self.stderr = None
        self.exit_code = None
        self.error = None

    def _run(self, wait=True):
        """Just run the local command and return the exit code. Also populate
        `output' and `exit_code' with the command's stdout and exit code.

        """

        try:
            args = shlex.split(self.command)
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=self.working_dir)
        except OSError:
            # It might be a shell builtin
            args = shlex.split("bash -i -c \"%s\"" % self.command)
            p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=self.working_dir)

        self.logger.info("Running '%s' in '%s'" % (self.command, self.working_dir))
        p.wait()
        self.stdout, self.stderr = p.communicate()
        self.exit_code = p.returncode

        if self.exit_code != self.expected_exit:
            self.error = "Expected exit code %d, got %d." % (self.expected_exit, self.exit_code)
            self.logger.error(self.error)

    def get_error(self):
        if self.error:
            return "Error: %s\nStderr: %s" % \
                (self.error, self.stderr)

    def get_output(self):
        return self.stdout

    def get_exit(self):
        return self.exit_code

    def get_title(self):
        return self.command

    def run(self):
        """ Run yourself.
        """

        self._run()


class MakeProcedure(Procedure):
    """ Runs make with various arguments. Is a bit smarter with errors
    than simple popen.
    """

    def __init__(self, directive="", conf=DEFAULT_SETTINGS, *args, **kwargs):
        """ Give the first directive.
	"""

        self.exit_to_error = conf.settings["MAKE_EXIT_TO_ERROR"]
        command = "%s %s" % (conf.settings["DEFAULT_MAKE_CMD"], directive)

        super(MakeProcedure, self).__init__(command, conf=conf, *args, **kwargs)


    def get_error(self):
        error = super(MakeProcedure, self).get_error()

        if self.exit_code in self.exit_to_error:
            if not error:
                error = ""

            return error + self.exit_to_error[self.exit_code]

        return error
