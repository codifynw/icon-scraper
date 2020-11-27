import os
import pathlib
from pathlib import Path
import re
from bs4 import BeautifulSoup

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
                    # self.scanFile(os.path.join(root, name))

    def scanFile(self, line):
        print('SCAN FILE FUNCTION')
        # print(self.newFilename)

if __name__ == '__main__':
    scriptPath = pathlib.Path(__file__).parent.absolute()
    scanObj = Parser(scriptPath)
