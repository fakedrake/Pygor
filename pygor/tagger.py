import os
import datetime

import git

from pygor.logger import Logger
from pygor.settings import DEFAULT_TAG_STRF_TEMPLATE, DEFAULT_PROJECT_ROOT
from pygor.procedure import Procedure

class Tagger(Logger):
    """ Add tags to the heads of objects
    """

    def __init__(self, repos, root=DEFAULT_PROJECT_ROOT):
        """Give a list of paths. These paths may be relative to a root path.

        """
        self.root = root
        self.repos = [repo_factory(os.path.join(self.root, r)) for r in repos]

    def flush(self):
        """ Flush the chanes to the server.
        """

        if r.is_dirty():
            raise ValueError("I mistakenly made some changes in the '%s' repo. Fix this." % repo.working_dir)

        r.push(tags=True)


        raise NotImplemented("Pushing the tags is not yet implemented.")


    def make_tag(self, repo, template=DEFAULT_TAG_STRF_TEMPLATE):
        """Create the tag name we are to create from current time."""
        repo.create_tag(datetime.datetime.now().strftime(template))

    def make_tags(self, template=DEFAULT_TAG_STRF_TEMPLATE):
        """Tag all branches"""
        for r in self.repos:
            self.make_tag(r, template)


class GITRepo(git.Repo):
    """A thin wrapper to make pushing tags a bit easier."""

    def push_tags(self):
        """ Push everything to remote. """
        o = self.remotes.origin
        o.push(tags=True)

    @staticmethod
    def is_repo(path):
        """ Check if this is the root of a git repo.
        """
        return git.repo.fun.is_git_dir(os.path.join(path, ".git"))

class CVSRepo(Logger):
    """Emulate the parts of git.Repo we need. Note that I do not trust a
    script to actually write anything to a CVS repository so I just
    pretend to do them.

    """

    @staticmethod
    def is_repo(path):
        return os.path.isdir(os.path.join(path, "CVS"))

    def __init__(self, path):
        self.working_dir = path

    def is_dirty(self):
        self.logger.info("Pretending to check if CVS repo '%s' is dirty." % self.working_path)
        return True

    def create_tag(self, tag_name):
        """Create a tag to the head with this name. Raises IOError if fail.

        """
        p = Procedure("cvs tag \"%s\"" % tag_name, working_dir=self.working_dir)
        p.run()

        if p.get_error():
            raise IOError("CVS failed to tag with error: %s" % p.get_error())

    def push_tags(self):
        """ Emulate the other push
        """
        self.logger.info("Pretending to push CVS repo '%s'." % self.working_path)


def repo_factory(path):
    """ Create a CVSRepo or a GITRepo object.
    """

    if GITRepo.is_repo(path):
        return GITRepo(path)

    if CVSRepo.is_repo(path):
        return CVSRepo(path)

    raise ValueError("%s doesnt seem to be any kind of repo.")
