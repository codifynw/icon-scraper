import os
import pathlib

def scanLine(line):
    print(line)
    # print("line {} contents {}".format(cnt, line))

def scanFile(filePath):
    print('scan')
    with open(filePath) as fp:
        for line in fp:
            scanLine(line)

def walk(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            scanFile(os.path.join(root, name))
        for name in dirs:
            print('folder')
            walk(os.path.join(root, name))

htmlPath = pathlib.Path(__file__).parent.absolute()
htmlPath = htmlPath / "static"
walk(htmlPath)
