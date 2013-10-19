import DimesExceptions
import Operation
from lxml import etree

class Script(object):
    """This class is responsible for the execution of a single DIMES script"""
    scriptPath = None
    xml = None
    id = None
    exid = None
    operationList = []
    def __init__(self, scriptPath):
        # Load the script into memory
        self.scriptPath = scriptPath
        self.xml = etree.parse(self.scriptpath)
        self.id = self.xml.find("Script").get("id")
        self.exid = self.xml.find("Script").get("ExID")
        
        # Parse the script operations
        operations = self.xml.find("Script").text.splitlines()
        for operation in operations:
            if len(operation) == 0:
                continue
            operation = operation.split()
            if operation[0] == "PING":
                self.operationList.append(Operation.PingOperation(operation[1]))
            elif operation[0] == "TRACEROUTE":
                self.operationList.append(Operation.TracerouteOperation(operation[1]))
            else:
                raise DimesExceptions.ScriptParseException("Unknown operation: %s" % operation[0])
        
        
    def execute(self):
        """Executes the loaded script"""
        print self.xml.find("Script").text