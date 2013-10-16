from lxml import etree
from lxml import objectify

class Script:
    """This class is responsible for the execution of a single DIMES script"""
    def __init__(self, scriptpath):
        # Load the script
        xml = etree.parse(scriptpath)
        self.id = xml.find("Script").get("id")
        self.exid = xml.find("Script").get("ExID")
        
    def dostuff(self):
        print self.id