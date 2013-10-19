from datetime import datetime
import socket

class Operation(object):
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
        # Look up the reverse DNS
        self.DestIP = address

    # 'Pythonic' abstraction...
    def execute(self):
        raise NotImplementedError()
    
    def _start(self):
        # Some common tasks that need to be done when an operation starts
        # Reverse DNS
        self.DestAddress = socket.gethostbyaddr(self.DestIP)[0]
        
        # Current time
        self.StartTime = str(datetime.utcnow()).strip("0")
        self.LocalStartTime = str(datetime.now()).strip("0")
    
    def output(self):
        raise NotImplementedError()
        
class PingOperation(Operation):
    CommandType = "PING"
    
    
class TracerouteOperation(Operation):
    CommandType = "TRACEROUTE"