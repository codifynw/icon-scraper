import os
import pathlib

def walk(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            print('crab')
            print(os.path.join(root, name))
        for name in dirs:
            print('folder')
            walk(os.path.join(root, name))

scriptPath = pathlib.Path(__file__).parent.absolute()
walk(scriptPath)
