from datetime import datetime
from util import Log
from util import Ping
import socket

class Operation(object):
    script = None
    
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
    
    def __init__(self, script, address):
        self.script = script
        self.DestIP = address

    def do(self):
        raise NotImplementedError()
    
    def _start(self):
        # Some common tasks that need to be done when an operation starts
        Log.log("Executing %s to address %s" % (self.CommandType, self.DestIP))
        # Reverse DNS
        try:
            self.DestAddress = socket.gethostbyaddr(self.DestIP)[0]
        except socket.herror:
            self.DestAddress = self.DestIP
        
        # Current time
        self.StartTime = str(datetime.utcnow()).strip("0")
        self.LocalStartTime = str(datetime.now()).strip("0")
    
    def output(self):
        raise NotImplementedError()



class PingOperation(Operation):
    CommandType = "PING"
    def do(self):
        self._start()
        delay = Ping.do_one(self.DestIP)
        Log.log("Response time for %s is %sms" % (self.DestIP, delay))



class TracerouteOperation(Operation):
    CommandType = "TRACEROUTE"
    def do(self):
        self._start()
        