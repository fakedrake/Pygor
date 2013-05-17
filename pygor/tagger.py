import os
import datetime

from git import Repo

from pygor.logger import Logger
from pygor.settings import DEFAULT_TAG_STRF_TEMPLATE, DEFAULT_PROJECT_ROOT

class Tagger(Logger):
    """ Add tags to the heads of objects
    """

    def __init__(self, repos, root=DEFAULT_PROJECT_ROOT):
        """Give a list of paths. These paths may be relative to a root path.

        """
        self.root = root
        self.repos = [Repo(os.path.join(self.root, r)) for r in repos]

    def flush(self):
        """ Flush the chanes to the server.
        """
        raise NotImplemented("Pushing the tags is not yet implemented.")


    def make_tag(self, repo, template=DEFAULT_TAG_STRF_TEMPLATE):
        """Create the tag name we are to create from current time."""
        repo.create_tag(datetime.datetime.now().strftime(template))

    def make_tags(self, template=DEFAULT_TAG_STRF_TEMPLATE):
        """Tag all branches"""
        for r in repos:
            self.make_tag(r, template)
