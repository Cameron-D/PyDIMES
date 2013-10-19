class Operation:
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
        self.DestIP = address

    # 'Pythonic' abstraction...
    def execute(self):
        raise NotImplementedError()
    
    def output(self):
        raise NotImplementedError()
        
class PingOperation(Operation):
    CommandType = "PING"
    
    
class TracerouteOperation(Operation):
    CommandType = "TRACEROUTE"