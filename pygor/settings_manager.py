import string
import yaml

import pygor.settings

class Settings(object):
    def __init__(self, fname="", args=None):
        """Create a config that will contain the final version of the module
        settings.

        """

        try:
            conf_file = yaml.load(open(fname).read())
        except IOError:
            conf_file = dict(settings={})

        settings_section = dict([(string.upper(k), v) for k,v in conf_file['settings'].iteritems()])
        data = pygor.settings.__dict__.copy()
        data.update(settings_section)
        self.settings = dict([(k,v) for k,v in data.iteritems() if k[:2] != "__" and k in dir(pygor.settings)])

        self.make_cmds = conf_file.get("make", [])
        self.spamtargets = conf_file.get("spamtargets", [])
        self.setup_cmds = conf_file.get("setup", [])
        self.cleanup_cmds = conf_file.get("cleanup", [])
        self.watched_repos = conf_file.get("watched_repos", [])

def updated_settings(old, **kwargs):
    if not kwargs:
        return old

    ret = old.copy()
    ret.update(dict([(string.upper(k), v) for k,v in kwargs.iteritems()]))
    return ret

DEFAULT_SETTINGS = Settings()
