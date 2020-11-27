import os
import pathlib
import re
from bs4 import BeautifulSoup

def writeResult(line):
    newFilename.write(line)

def updateLine(line, soup):
    # TODO: add new icon class, remove data-icon
    # writeResult(line)
    return("THIS LINE WILL BE CHANGED")

def getClasses(line, soup):
    return [line["class"] for line in soup.find_all() if "class" in line.attrs]

def getIconValue(line, soup):
    return [line["data-icon"] for line in soup.find_all() if "data-icon" in line.attrs]

def lookForIcon(line):
    if line.find("data-icon") > -1:
        soup = BeautifulSoup(line, 'html.parser')
        iconValue = getIconValue(line, soup)
        classResult = getClasses(line, soup)
        if classResult:
            writeResult(updateLine(line, soup))
        else:
            print('element has no class - note exception')
            writeResult(line)
    else:
        writeResult(line)

def scanLine(line):
    lookForIcon(line)

def scanFile(filePath):
    print(filePath)
    with open(filePath) as fp:
        for line in fp:
            scanLine(line)

def scanDir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.split('.')[1] == 'html':
                newFilename = open(name, "w+")
                scanFile(os.path.join(root, name))
        for name in dirs:
            scanDir(os.path.join(root, name))

if __name__ == '__main__':
    scriptPath = pathlib.Path(__file__).parent.absolute()
    srcPath = scriptPath / "static"
    distPath = scriptPath / "__dist/"
    scanDir(srcPath)
