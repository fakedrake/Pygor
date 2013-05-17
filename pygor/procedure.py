import os
import shlex
from subprocess import Popen, PIPE

from pygor.settings import MAKE_EXIT_TO_ERROR, \
    DEFAULT_MAKE_CMD

class Procedure(object):
    """ Subclass this to create a procedure that the Big Machine can run.
    """

    def __init__(self, command, expected_exit=0, parametrizer=lambda proc: dict(), working_dir=None):
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
        self.parametrizer = parametrizer
        self.working_dir = working_dir

        self.stdout = None
        self.stderr = None
        self.exit_code = None
        self.error = None

    def _run(self, wait=True):
        """Just run the local command and return the exit code. Also populate
        `output' and `exit_code' with the command's stdout and exit code.

        """

        final_cmd = self.command % self.parametrizer(self)
        args = shlex.split(final_cmd)
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=self.working_dir)
        p.wait()
        self.stdout, self.stderr = p.communicate()
        self.exit_code = p.returncode

    def get_error(self):
        return self.error

    def get_output(self):
        return self.stdout

    def get_exit(self):
        return self.exit_code

    def run(self):
        """ Run yourself.
        """

        self._run()


class MakeProcedure(Procedure):
    """ Runs make with various arguments. Is a bit smarter with errors
    than simple popen.
    """

    def __init__(self, directive="", exit_to_error=MAKE_EXIT_TO_ERROR, make_command=DEFAULT_MAKE_CMD, *args, **kwargs):
        """ Give the first directive.
	"""

        self.exit_to_error = exit_to_error
        command = "%s %s" % (make_command, directive)

        super(MakeProcedure, self).__init__(command, *args, **kwargs)


    def get_error(self):
        error = super(MakeProcedure, self).get_error()

        if self.exit_code in self.exit_to_error.keys():
            if not error:
                error = ""

            return error + self.exit_to_error[self.exit_code]

        return error
