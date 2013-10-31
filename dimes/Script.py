from lxml import etree
from util import Log
from util import Config
import threading, time
import Exceptions, PingOperation, TracerouteOperation, Worker, Queue

class Script(object):
    """This class is responsible for the execution of a single DIMES script"""
    scriptPath = None
    xml = None
    id = None
    exid = None
    operationQ = Queue.Queue()
    operationQlock = threading.Lock()
    resultQ = Queue.Queue()
    
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
                op = PingOperation.PingOperation(self, operation[1])
            elif operation[0] == "TRACEROUTE":
                op = TracerouteOperation.TracerouteOperation(self, operation[1])
            else:
                raise Exceptions.ScriptParseException("Unknown operation: %s in script %s, PLEASE REPORT THIS!" %
                                                           (operation[0], self.scriptPath))
            self.operationQ.put(op)
        Log.log("Loaded script %s, %d operations to run" % (self.scriptPath, self.operationQ.qsize()), 1)
        
    def execute(self):
        """Executes the loaded script"""
        for i in range(Config.config.getint("Performance", "ParallelWorkers")):
            w = Worker.Worker(self)
            w.setDaemon(True)
            w.start()
            time.sleep(Config.config.getint("Performance", "ThreadStartDelay") / 1000.0)
            
        return True