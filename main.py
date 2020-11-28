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

    def getAttributes(self):
        return [line["data-icon"] for line in self.soup.find_all() if "data-icon" in line.attrs]

    def clean(self, file):
        attributes = self.getAttributes()
        if attributes:
            for attribute in list(set(attributes)):
                newClassName = self.mapIconClassFromAttr(attribute)
                elementsWithAttribute = self.getElementByAttribute(attribute)
                for element in elementsWithAttribute:
                    classes = element.get_attribute_list('class')
                    if newClassName:
                        if None in classes:
                            print('if')
                            print('classes: ', classes)
                            element['class'] = 'show-icon icon-' + newClassName
                        else:
                            print('else')
                            print('classes: ', classes)
                            element['class'] = ' '.join(map(str, element.get_attribute_list('class'))) + ' ' + 'show-icon' + ' ' + 'icon-' + newClassName
            self.removeAttr()
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
                    if file.split('.')[1] == 'html':
                        self.outerParser.createNewFile(root,file)
                        self.scan.file(os.path.join(root, file))

        def file(self, filePath):
            with open(filePath) as file:
                self.outerParser.makeSoup(file)
                self.outerParser.clean(file)

    def makeSoup(self, file):
        self.soup = BeautifulSoup(file, 'html.parser')

    def createNewFile(self, root, file):
        pathInStatic = root.split('icon-scraper/static/')[1]
        newFilePath = os.path.join(self.distPath,pathInStatic)
        Path(newFilePath).mkdir(parents=True, exist_ok=True)
        self.newFile = open(os.path.join(newFilePath,file), "w+")

    def soup_prettify2(self, soup, desired_indent): #where desired_indent is number of spaces as an int()
    	pretty_soup = str()
    	previous_indent = 0
    	for line in soup.prettify().split("\n"): # iterate over each line of a prettified soup
    		current_indent = str(line).find("<") # returns the index for the opening html tag '<'
    		# which is also represents the number of spaces in the lines indentation
    		if current_indent == -1 or current_indent > previous_indent + 2:
    			current_indent = previous_indent + 1
    			# str.find() will equal -1 when no '<' is found. This means the line is some kind
    			# of text or script instead of an HTML element and should be treated as a child
    			# of the previous line. also, current_indent should never be more than previous + 1.
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
        self.newFile.write(self.soup_prettify2(self.soup, desired_indent=4))

    def removeAttr(self):
        for tag in self.soup.find_all(lambda t: any(i.startswith('data-') for i in t.attrs)):
            for attr in list(tag.attrs):
                if attr.startswith('data-icon'):
                    del tag.attrs[attr]

    def find(self, iconValue):
        for x in iconMap:
            if x["oldCode"] == iconValue:
                return x["className"]

    def mapIconClassFromAttr(self, iconValue):
        if iconValue:
            newClassName = self.find(iconValue)
        else:
            newClassName = False
        return newClassName

if __name__ == '__main__':
    scriptPath = pathlib.Path(__file__).parent.absolute()
    scanObj = Parser(scriptPath)
