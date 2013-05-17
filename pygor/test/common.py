import os

TEST_DIR = os.path.dirname(__file__)

def in_resources(filename):
    return os.path.join(TEST_DIR, "resources", filename)
