import os
import pathlib
import re

def lookForIcon(line):
    if line.find("data-icon") > -1:
        lst = re.findall(r'"(.*?)(?<!\\)"', line)
        print(line)
        print(lst)

def scanLine(line):
    lookForIcon(line)

def scanFile(filePath):
    print('scan')
    with open(filePath) as fp:
        for line in fp:
            scanLine(line)

def scanDir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            scanFile(os.path.join(root, name))
        for name in dirs:
            print('folder')
            scanDir(os.path.join(root, name))

htmlPath = pathlib.Path(__file__).parent.absolute()
htmlPath = htmlPath / "static"
scanDir(htmlPath)
