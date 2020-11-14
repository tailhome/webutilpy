# -*- coding: utf-8 -*-

from html.parser import HTMLParser

# abstract element class
class Element:
    NOVALUE = '*novalue*'
    NONAME = '*noname*'

    def parse(self, reader, builder):
        raise('this method should not be invoked')

    def isTagElement(self):
        return False

    def getName(self):
        return Element.NONAME;

    def getText(self):
        return Element.NOVALUE;

class PlainText(Element):

    def __init__(self, text = ''):
        self.text = text

    def getRawText(self):
        return self.text

    def getText(self):
        return self.text.lstrip().rstrip()

    def setText(self, text):
        self.text = text

class TagElement(Element):

    def __init__(self, name, closeTag = False):
        self.closeTag = closeTag
        self.name = name
        self.attributes = {}

    def isTagElement(self):
        return True

    def isCloseTag(self):
        return self.closeTag

    def getName(self):
        return self.name

    def quoteTrim(source):
        text = source
        if len(source) > 2:
            text = ''.join(source).strip('"\'')
        return text

    def getAttribute(self, name):
        value = None
        if len(self.attributes) > 0:
            lname = name.lower()
            if lname in self.attributes:
                value = TagElement.quoteTrim(self.attributes[lname])
        return value

    def setAttributes(self, attrs):
        for attr in attrs:
            lattr = attr[0].lower()
            if attr[1] is not None:
                lvalue = attr[1].lower()
                self.attributes[lattr] = lvalue
            else:
                self.attributes[lattr] = None

# 
class HTMLReader(HTMLParser):
    # elements = NULL

    def __init__(self):
        super(HTMLReader, self).__init__()
        self.elements = [];

    def handle_starttag(self, tag, attrs):
        element = TagElement(tag)
        element.setAttributes(attrs)
        self.elements.append(element)

    def handle_endtag(self, tag):
        element = TagElement(tag, True)
        self.elements.append(element)

    def handle_data(self, data):
        stripped = data.strip()
        if len(stripped) == 0:
            return
        element = PlainText(data)
        self.elements.append(element)

    def size(self):
        return len(self.elements)

    def getElement(self, index):
        if index < 0 or index >= len(self.elements):
            return None
        return self.elements[index]

    # def findTagOf(self, name, startIndex = 0):
    #    index = self.findTagIndexOf(name, startIndex)
    #    if index < 0:
    #        return None
    #    return self.elements[index]

    def findTagIndexOf(self, name, startIndex = 0, attrName = None, attrValue = None):
        lname = name.lower()
        lattrName = None
        lattrValue = None
        # check parameter
        if attrName is not None:
            if attrValue is None:
                return -1
            lattrName = attrName.lower()
            lattrValue = attrValue.lower()
        # check elements size
        size = len(self.elements)
        if size < 1 or startIndex < 0:
            return -1           # out of bounds
        retIndex = -1
        for i in range(startIndex, size):
            element = self.elements[i]
            if element.isTagElement():
                if element.getName().lower() == lname:
                    if attrName is None:
                        retIndex = i
                        break
                    lvalue = element.getAttribute(lattrName)
                    if lattrValue == lvalue:
                        retIndex = i
                        break
        return retIndex

    def findPlainTextIndex(self, substr, startIndex = 0):
        size = len(self.elements)
        if size < 1 or startIndex < 0:
            return -1           # out of bounds
        retIndex = -1
        for i in range(startIndex, size):
            if not self.elements[i].isTagElement():
                if substr in self.elements[i].getText():
                    retIndex = i
                    break
        return retIndex

    def getNextPlainTextIndex(self, startIndex = -1):
        size = len(self.elements)
        if size < 1 or startIndex < -1 or size < startIndex+1:
            return -1           # out of bounds
        retIndex = -1
        for i in range(startIndex + 1, size):
            if not self.elements[i].isTagElement():
                retIndex = i
                break
        return retIndex

