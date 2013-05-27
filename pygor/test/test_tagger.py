import os
import unittest
import git
import subprocess

from pygor.test.common import in_resources, snapshot_resources, clean_resources
from pygor.tagger import Tagger

GIT_REPO = in_resources("DummyGit")
REPO_FILE = os.path.join(GIT_REPO, "test.txt")
TAG_TEMPLATE = "Release-%Y.%m.%d-%H.%M.%S"

class TestTagger(unittest.TestCase):
    def setUp(self):
        """Setup a dummy git repository with two commits.

        """
        snapshot_resources()

        self.repo = git.Repo.init(GIT_REPO)

        # Commit a file
        open(REPO_FILE, "w").write("hello world")
        self.repo.index.add([REPO_FILE])
        self.repo.index.commit("Initial commit")

        # Add another commit
        open(REPO_FILE, "w").write("Hello world!")
        self.repo.index.commit("Slightly better formating")

    def tearDown(self):
        """Completely delete the repo.

        """
        clean_resources()

    def test_tagger(self):
        self.tagger = Tagger([GIT_REPO], default_project_root=in_resources())
        self.tagger.make_tags()
        self.assertIn("Release-", self.repo.tags[0].name)
