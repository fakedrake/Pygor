from datetime import datetime

from pygor.procedure import Procedure, MakeProcedure
from pygor.settings_manager import DEFAULT_SETTINGS, update_settings


def generate_id(id_template):
    """ Generate an id for the big machine.
    """

    return datetime.now().strftime(id_template)


class BigMachine(object):
    """Plug into this class the processes that are to be run
    successfully. If they fail the big machine wil tell Pygor what
    went wrong.

    """

    def __init__(self, conf=DEFAULT_SETTINGS, **kwargs):
        """Provide some procedures for testing and cleanup. You may also
        provide an identifier which is used as-is as a directory
        name. By default cleanup is removing the directory that would
        otherwise be created. The working dir is the default dir that
        we use when creating new processes.

        """
        self.settings = updated_settings(conf.settings, **kwargs)

        self.identifier = generate_id(self.settings["ID_TEMPLATE"])
        try:
            self.working_dir = os.path.join(self.settings["WORKING_DIR"], self.identifier)
        except AttributeError:
            self.working_dir = None

        self.context = dict(machine_id=self.identifier, pwd=(self.working_dir))

        self.procedures = conf.setup_cmds
        for p in self.procedures:
            p.command = p.command % self.context

        self.cleanup_procedures = [Procedure(c % self.context, working_dir=working_dir) for c in conf.cleanup_cmds]

        self.reset()


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
                self.stdout = p.get_output()
                return self.stdout

        return None

    def get_error(self):
        """ Get error. If squeky return none.
        """
        return self.error


    def add_test(self, procedure, proc_type=MakeProcedure):
        """Test procedures are usually makefiles so we might aswell read them
        by name."""

        if isinstance(procedure, str):
            self.procedures.append(MakeProcedure(procedure % self.context, working_dir=self.working_dir))
        else:
            self.procedures.append(procedure)

    def reset(self, procedures=False):
        """ Reset to a state as if it had never run.
        """
        self._ran = False
        self.exit_code = None
        self.stdout = None
        self.stderr = None
        self.error = None

        if procedures:
            self.procedures = []
