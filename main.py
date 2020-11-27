import os
import pathlib
from pathlib import Path
import re
from bs4 import BeautifulSoup

from iconMap import iconMap

class Parser:
    def __init__(self, scriptPath):
        self.definePaths(scriptPath)
        self.scanStatic()

    def definePaths(self, scriptPath):
        self.srcPath = scriptPath / "static"
        self.distPath = scriptPath / "__dist/"

    def scanStatic(self):
        for root, dirs, files in os.walk(self.srcPath, topdown=False):
            for file in files:
                if file.split('.')[1] == 'html':
                    path_file = os.path.join(root,file)
                    pathInStatic = root.split('icon-scraper/static/')[1]
                    filePath = os.path.join(self.distPath,pathInStatic)
                    Path(filePath).mkdir(parents=True, exist_ok=True)
                    self.newFile = open(os.path.join(filePath,file), "w+")
                    self.scanFile(os.path.join(root, file))

    def scanFile(self, filePath):
        with open(filePath) as fp:
            for line in fp:
                self.scanLine(line)

    def scanLine(self, line):
        self.lookForIcon(line)

    def lookForIcon(self, line):
        if line.find("data-icon") > -1:
            soup = BeautifulSoup(line, 'html.parser')
            classResult = self.getClasses(line, soup)
            if classResult:
                self.updateLine(line, soup)
            else:
                self.addClassToLine(line,soup)
        else:
            self.writeResult(line)

    def writeResult(self, line):
        self.newFile.write(line)

    def addClassToLine(self, line, soup):
        self.writeResult('THIS LINE WILL BE CHANGED')

    def removeAttr(self,soup):
        for tag in soup.find_all(lambda t: any(i.startswith('data-') for i in t.attrs)):
            for attr in list(tag.attrs):
                if attr.startswith('data-icon'):
                    del tag.attrs[attr]
        return soup

    def updateLine(self, line, soup):
        newClassName = self.mapIconClassFromAttr(line, soup)
        if newClassName:
            soup.find("div")['class'] = ' '.join(map(str, self.getClasses(line, soup)[0])) + ' ' + 'show-icon' + ' ' + 'icon-' + newClassName
            soup = self.removeAttr(soup)
            self.writeResult(str(soup))

    def find(self, arr , iconValue):
        for x in arr:
            if x["oldCode"] == iconValue:
                return x["className"]

    def getClasses(self, line, soup):
        return [line["class"] for line in soup.find_all() if "class" in line.attrs]

    def getIconValue(self, line, soup):
        return [line["data-icon"] for line in soup.find_all() if "data-icon" in line.attrs]

    def mapIconClassFromAttr(self, line, soup):
        iconValue = self.getIconValue(line, soup)
        newClassName = self.find(iconMap , iconValue[0])
        return newClassName

if __name__ == '__main__':
    scriptPath = pathlib.Path(__file__).parent.absolute()
    scanObj = Parser(scriptPath)
