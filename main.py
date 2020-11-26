import os
import pathlib

def walk(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print('folder')
            walk(os.path.join(root, name))

htmlPath = pathlib.Path(__file__).parent.absolute()
htmlPath = htmlPath / "static"
walk(htmlPath)
