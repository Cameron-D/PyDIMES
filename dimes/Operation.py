from datetime import datetime
import threading
import socket

class Operation(threading.Thread):
    # All the values a script is required to return
    ExID = None
    ScriptID = None
    Priority = "NORMAL"
    ScriptLineNum = -1
    StartTime = None
    LocalStartTime = None
    CommandType = None
    Protocol = "ICMP"
    SourceName = None
    DestName = None
    DestIP = None
    DestAddress = None
    NumOfTrials = None
    Success = False
    reachedDest = False
    Exceptions = ""
    
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.DestIP = address

    # 'Pythonic' abstraction...
    def run(self):
        raise NotImplementedError()
    
    def _start(self):
        # Some common tasks that need to be done when an operation starts
        print "Executing %s to address %s" % (self.CommandType, self.DestIP)
        # Reverse DNS
        self.DestAddress = socket.gethostbyaddr(self.DestIP)[0]
        
        # Current time
        self.StartTime = str(datetime.utcnow()).strip("0")
        self.LocalStartTime = str(datetime.now()).strip("0")
    
    def output(self):
        raise NotImplementedError()
        
class PingOperation(Operation):
    CommandType = "PING"
    def run(self):
        self._start()
    
class TracerouteOperation(Operation):
    CommandType = "TRACEROUTE"