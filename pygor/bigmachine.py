from pygor.procedure import Procedure
from pygor.settings import DEFAULT_MACHINE_ID_TEMPLATE

def generate_id(id):
    """ Generate an id for the big machine.
    """

    if id is None:
        return datetime.now().strftime(DEFAULT_MACHINE_ID_TEMPLATE)

    return id


class BigMachine(object):
    """Plug into this class the processes that are to be run
    successfully. If they fail the big machine wil tell Pygor what
    went wrong.

    """

    def __init__(self, procedures=[], cleanup_procedures=[], identifier=None, working_dir=None):
        """Provide some procedures for testing and cleanup. You may also
        provide an identifier.

        """
        self.identifier = generate_id(identifier)

        self.working_dir = working_dir
        self.procedures = procedures

        if cleanup_procedures:
            self.cleanup_procedures = cleanup_procedures
        else:
            self.cleanup_procedures = [Procedure("rm -rf %s" %
                                                 self.identifier, working_dir=working_dir)]

        self.error = None
        self.stdout = stdout

    def cleanup(self):
        """Undo whatever would be done. Typically remove the directory that
        would be created. Get errors to check state.

        """

        return self._run(self.cleanup_procedures)

    def setup(self):
        """Setup the environment for running."""

        self._setup = True

        if not self.get_error():
            return self._run(self.procedures)

        raise EnvironmentError("There have been errors during previous run of BigMachine.")


    def run(self):
        """Run tests."""

        if not self._setup:
            self.setup()

        if not self.get_error():
            return self._run(self.procedures)

        raise EnvironmentError("There have been errors during previous run of BigMachine.")

    def _run(self, procedures):
        """ Run the tests one by one.
        """
        for p in procedures:
            p.run()

            if p.get_error() is not None:
                self.error = t.get_error()
                self.stdout = t.stdout
                return t.stdout

        return None

    def get_error(self):
        """ Get error. If squeky return none.
        """
        return self.error


    def add_test(self, procedure, proc_type=MakeProcedure):
        """Test procedures are usually makefiles so we might aswell read them
        by name."""

        if isinstance(procedure, str):
            self.procedures.append(MakeProcedure(procedure))
        else:
            self.procedures.append(procedure)
