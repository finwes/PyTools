import xml.etree.ElementTree as ET

class PCParser(ET.XMLTreeBuilder):

   def __init__(self):
       ET.XMLTreeBuilder.__init__(self)
       self._parser.CommentHandler = self.handle_comment

   def handle_comment(self, data):
       self._target.start(ET.Comment, {})
       self._target.data(data)
       self._target.end(ET.Comment)

class Config:
    def __init__(self):
        parser = PCParser()
        self.configXML = ET.parse('config.xml', parser=parser)

    def getAttribute(self, name):
        element = self.configXML.getroot().find(name)
        return element.text

    def setAttribute(self, name, value):
        element = self.configXML.getroot().find(name)
        element.text = value

    def save(self):
        self.configXML.write('config.xml')