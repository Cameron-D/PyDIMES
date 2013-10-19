import DimesExceptions
import Operation
import Queue
import Worker
import threading
from util import Log
from lxml import etree

class Script(object):
    """This class is responsible for the execution of a single DIMES script"""
    scriptPath = None
    xml = None
    id = None
    exid = None
    operationQ = Queue.Queue()
    operationQlock = threading.Lock()
    
    def __init__(self, scriptPath):
        # Load the script into memory
        self.scriptPath = scriptPath
        self.xml = etree.parse(self.scriptPath)
        self.id = self.xml.find("Script").get("id")
        self.exid = self.xml.find("Script").get("ExID")
        
        # Parse the script operations
        operations = self.xml.find("Script").text.splitlines()
        for operation in operations:
            if len(operation) == 0:
                continue
            operation = operation.split()
            if operation[0] == "PING":
                op = Operation.PingOperation(self, operation[1])
            elif operation[0] == "TRACEROUTE":
                op = Operation.TracerouteOperation(self, operation[1])
            else:
                raise DimesExceptions.ScriptParseException("Unknown operation: %s" % operation[0])
            self.operationQ.put(op)
        Log.log("Loaded script %s, %d operations to run" % (self.scriptPath, self.operationQ.qsize()))
        
    def execute(self):
        """Executes the loaded script"""
        for i in range(16):
            w = Worker.Worker(self)
            w.start()
        return True