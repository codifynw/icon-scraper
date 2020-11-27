import os
import pathlib
from pathlib import Path
import re
from bs4 import BeautifulSoup

from iconMap import iconMap

class Parser:
    def __init__(self, scriptPath):
        self.scan = self.Scan(self)
        self.definePaths(scriptPath)
        self.scan.staticDir()

    def definePaths(self, scriptPath):
        self.srcPath = scriptPath / "static"
        self.distPath = scriptPath / "__dist/"

    class Scan:
        def __init__(self, parser):
            self.outerParser = parser
            self.scan = self

        def staticDir(self):
            for root, dirs, files in os.walk(self.outerParser.srcPath, topdown=False):
                for file in files:
                    if file.split('.')[1] == 'html':
                        path_file = os.path.join(root,file)
                        pathInStatic = root.split('icon-scraper/static/')[1]
                        filePath = os.path.join(self.outerParser.distPath,pathInStatic)
                        Path(filePath).mkdir(parents=True, exist_ok=True)
                        self.outerParser.newFile = open(os.path.join(filePath,file), "w+")
                        self.scan.file(os.path.join(root, file))

        def file(self, filePath):
            with open(filePath) as fp:
                for line in fp:
                    self.scan.line(line)

        def line(self, line):
            soup = self.outerParser.makeSoup(line)
            self.outerParser.updateLine(line, soup)

    def makeSoup(self, line):
        soup = BeautifulSoup(line, 'html.parser')
        return soup

    def writeResult(self, newLine):
        self.newFile.write(newLine)

    def removeAttr(self,soup):
        for tag in soup.find_all(lambda t: any(i.startswith('data-') for i in t.attrs)):
            for attr in list(tag.attrs):
                if attr.startswith('data-icon'):
                    del tag.attrs[attr]
        return soup

    def updateLine(self, line, soup):
        newClassName = self.mapIconClassFromAttr(line, soup)
        if newClassName:
            if self.getClasses(line, soup):
                soup.find("div")['class'] = ' '.join(map(str, self.getClasses(line, soup)[0])) + ' ' + 'show-icon' + ' ' + 'icon-' + newClassName
            else:
                soup.find("div")['class'] = 'show-icon icon-' + newClassName
            soup = self.removeAttr(soup)
            self.writeResult(str(soup))
        else:
            self.writeResult(line)

    def find(self, arr , iconValue):
        for x in arr:
            if x["oldCode"] == iconValue:
                return x["className"]

    def getClasses(self, line, soup):
        print('getClasses: ', [line["class"] for line in soup.find_all() if "class" in line.attrs])
        return [line["class"] for line in soup.find_all() if "class" in line.attrs]

    def getIconValue(self, line, soup):
        return [line["data-icon"] for line in soup.find_all() if "data-icon" in line.attrs]

    def mapIconClassFromAttr(self, line, soup):
        iconValue = self.getIconValue(line, soup)
        if iconValue:
            newClassName = self.find(iconMap , iconValue[0])
        else:
            newClassName = False
        return newClassName

if __name__ == '__main__':
    scriptPath = pathlib.Path(__file__).parent.absolute()
    scanObj = Parser(scriptPath)
