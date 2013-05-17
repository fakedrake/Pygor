import os
import unittest
import git

from pygor.test.common import in_resources
from pygor.tagger import Tagger

GIT_REPO = in_resources("DummyGit")
REPO_FILE = os.path.join(GIT_REPO, "test.txt")
TAG_TEMPLATE = "Release-%Y.%m.%d-%H.%M.%S"

class TestMakeProcedure(unittest.TestCase):
    def setUp(self):
        """Setup a dummy git repository with two commits.

        """
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
        subprocess.call(["rm", "-rf", GIT_REPO])


    def test_tagger(self):
        self.tagger = Tagger([GIT_REPO], in_resources())
        self.tagger.make_tags()
        assertIn("Release-", self.repo.tags[0])
