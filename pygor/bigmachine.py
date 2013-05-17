from pygor.procedure import Procedure
from pygor.settings import DEFAULT_MACHINE_ID_TEMPLATE, \
    DEFAULT_PROJECT_ROOT

def generate_id(id, id_template=DEFAULT_MACHINE_ID_TEMPLATE):
    """ Generate an id for the big machine.
    """

    if id is None:
        return datetime.now().strftime(id_template)

    return id


class BigMachine(object):
    """Plug into this class the processes that are to be run
    successfully. If they fail the big machine wil tell Pygor what
    went wrong.

    """

    def __init__(self, procedures=[], cleanup_procedures=[], working_dir=DEFAULT_WORKING_DIR, id=None, id_template=DEFAULT_MACHINE_ID_TEMPLATE):
        """Provide some procedures for testing and cleanup. You may also
        provide an identifier which is used as-is as a directory
        name. By default cleanup is removing the directory that would
        otherwise be created.

        """
        self.identifier = generate_id(id, id_template)

        self.working_dir = working_dir
        self.procedures = procedures

        if cleanup_procedures:
            self.cleanup_procedures = cleanup_procedures
        else:
            self.cleanup_procedures = [Procedure("rm -rf %s" %
                                                 self.identifier, working_dir=working_dir)]

        self.error = None
        self.stdout = stdout
        self._ran = False

    def cleanup(self):
        """Undo whatever would be done. Typically remove the directory that
        would be created. Get errors to check state.

        """

        return self._run(self.cleanup_procedures)

    def run(self):
        """Run tests."""

        if not self.get_error():
            return self._run(self.procedures)

        raise EnvironmentError("There have been errors during previous run of BigMachine.")

    def _run(self, procedures):
        """ Run the tests one by one.
        """
        self._ran = True

        for p in procedures:
            p.run()

            if p.get_error() is not None:
                self.error = dict(error_title=p.get_title(), error_body=p.get_error())
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
