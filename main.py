import os
import pathlib
from pathlib import Path
import json
import re
from bs4 import BeautifulSoup
from iconMap import iconMap
import shutil

class Parser:
    def __init__(self, scriptPath):
        self.scan = self.Scan(self)
        self.definePaths(scriptPath)
        self.scan.staticDir()

    def definePaths(self, scriptPath):
        self.srcPath = scriptPath / "originalStatic"
        self.distPath = scriptPath / "__dist/"

    def getAttributes(self, soup):
        print('     ')
        print('     ')
        print('     ')
        print('     ')
        print('     ')
        print('     ')
        # data = json.loads(s[3].string)
        # print(data)
        # print(self.soup)
        # print('self.soup:', self.soup.find_all(attrs={"name" : "data-icon"}))
        print('     ')
        print('     ')
        print('     ')
        print('     ')
        print('     ')
        print('     ')
        return [line["data-icon"] for line in soup.find_all() if "data-icon" in line.attrs]

    def clean(self, soup):
        attributes = self.getAttributes(soup)
        print('**** ***** START **** *****')
        print('ATTRIBUTES')
        print('ATTRIBUTES', attributes)
        print('ATTRIBUTES')
        print('**** ***** STOP **** *****')
        if attributes:
            for attribute in list(set(attributes)):
                newClassName = self.mapIconClassFromAttr(attribute)
                elementsWithAttribute = self.getElementByAttribute(attribute)
                for element in elementsWithAttribute:
                    classes = element.get_attribute_list('class')
                    if newClassName:
                        if None in classes:
                            element['class'] = 'show-icon icon-' + newClassName
                        else:
                            element['class'] = ' '.join(map(str, element.get_attribute_list('class'))) + ' ' + 'show-icon' + ' ' + 'icon-' + newClassName
                        del element.attrs["data-icon"]
        self.writeResult()

    def getElementByAttribute(self, attribute):
        return [item for item in self.soup.find_all(attrs={'data-icon' : attribute})]

    class Scan:
        def __init__(self, parser):
            self.outerParser = parser
            self.scan = self

        def staticDir(self):
            for root, dirs, files in os.walk(self.outerParser.srcPath, topdown=False):
                for file in files:
                    print('file: ', file)
                    if file.split('.')[-1] == 'html':
                        self.outerParser.createNewFile(root,file)
                        self.scan.file(os.path.join(root, file))
                    else:
                        # simply copy
                        self.outerParser.simplyCopy(root,file)


        def file(self, filePath):
            with open(filePath) as file:
                soup = self.outerParser.makeSoup(file)
                self.outerParser.clean(soup)
                s = soup.find_all('script')
                # innerSoup = self.soup.find_all('script')
                innerString = s[0].string
                print('/////////')
                print(s[0].string)
                print('/////////')
                innerSoup = BeautifulSoup(innerString, 'html.parser')
                innerSoup = self.outerParser.clean(innerSoup)
                print(innerSoup)

    def makeSoup(self, file):
        self.soup = BeautifulSoup(file, 'html.parser')
        return self.soup

    def createNewFile(self, root, file):
        pathInStatic = root.split('icon-scraper/originalStatic/')[1]
        newFilePath = os.path.join(self.distPath,pathInStatic)
        Path(newFilePath).mkdir(parents=True, exist_ok=True)
        self.newFile = open(os.path.join(newFilePath,file), "w+")

    def soup_prettify2(self, soup, desired_indent):
    	pretty_soup = str()
    	previous_indent = 0
    	for line in soup.prettify().split("\n"):
    		current_indent = str(line).find("<")
    		if current_indent == -1 or current_indent > previous_indent + 2:
    			current_indent = previous_indent + 1
    		previous_indent = current_indent
    		pretty_soup += self.write_new_line(line, current_indent, desired_indent)
    	return pretty_soup

    def write_new_line(self, line, current_indent, desired_indent):
    	new_line = ""
    	spaces_to_add = (current_indent * desired_indent) - current_indent
    	if spaces_to_add > 0:
    		for i in range(spaces_to_add):
    			new_line += " "
    	new_line += str(line) + "\n"
    	return new_line

    def writeResult(self):
        self.newFile.write(str(self.soup))
        # self.newFile.write(self.soup_prettify2(self.soup, desired_indent=4))

    def simplyCopy(self, root, fileName):
        originalPath = os.path.join(root,fileName)
        newFilePath = os.path.join(root,fileName).replace('originalStatic', '__dist')
        os.makedirs(os.path.dirname(newFilePath), exist_ok=True)
        shutil.copyfile(originalPath, newFilePath)

    def removeAttr(self):
        for tag in self.soup.find_all(lambda t: any(i.startswith('data-') for i in t.attrs)):
            for attr in list(tag.attrs):
                if attr.startswith('data-icon'):
                    del tag.attrs[attr]

    def find(self, iconValue):
        for x in iconMap:
            if 'oldIcon' in x:
                if x["oldIcon"] == iconValue:
                    return x["className"]
            # else:
                # print('FOUND ELEMENT WITHOUT CODE IN MAP: ', iconValue)

    def mapIconClassFromAttr(self, iconValue):
        if iconValue:
            newClassName = self.find(iconValue)
        else:
            newClassName = False
        return newClassName

if __name__ == '__main__':
    scriptPath = pathlib.Path(__file__).parent.absolute()
    scanObj = Parser(scriptPath)
