import sys
import os

def env_init():
    # Append diff-gaussian-rasterization to the Python path
    sys.path.append(os.path.join(os.path.dirname(__file__), "diff-gaussian-rasterization"))

    # Optionally, append other subdirectories that might contain scripts to be imported
    sys.path.append(os.path.join(os.path.dirname(__file__), "guidance"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "simple-knn"))