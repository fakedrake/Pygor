import os
import shutil

TEST_DIR = os.path.dirname(__file__)
useful_dirs = []

def in_resources(filename=""):
    global useful_dirs
    ret = os.path.abspath(os.path.join(TEST_DIR, "resources", filename))

    return ret


def snapshot_resources():
    global useful_dirs
    useful_dirs = [in_resources(f) for f in
                   os.listdir(os.path.join(TEST_DIR, "resources"))]

def clean_resources():
    files = [in_resources(f) for f in
             os.listdir(os.path.join(TEST_DIR, "resources")) if in_resources(f) not in useful_dirs]

    for f in files:
        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)
