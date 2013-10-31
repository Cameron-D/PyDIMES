from datetime import datetime
from util import Ping
from util import Log
from util import Config
from util import IP
import socket, time

class Operation(object):
    script = None
    
    file = logfile = open('pydimes.log', 'a')
    
    # All the values a script is required to return
    Priority = "NORMAL"
    ScriptLineNum = -1
    StartTime = None
    LocalStartTime = None
    CommandType = None
    Protocol = "ICMP"
    DestName = None
    DestIP = None
    DestAddress = None
    NumOfTrials = None
    Success = False
    reachedDest = False
    Exceptions = ""
    RawDetails = {}
    
    def __init__(self, script, address):
        self.script = script
        self.DestIP = address

    def do(self):
        raise NotImplementedError()
    
    def _start(self):
        # Some common tasks that need to be done when an operation starts
        Log.log("Executing %s to %s" % (self.CommandType, self.DestIP))
        
        self.DestName = IP.reverseDNS(self.DestIP)
        self.DestAddress = IP.ip2int(self.DestIP)
        
        # Current time
        self.StartTime = str(datetime.utcnow()).strip("0")
        self.LocalStartTime = str(datetime.now()).strip("0")
    
    def getResult(self):
        result = {}
        result["ExID"] = self.script.exid
        result["ScriptID"] = self.script.id
        result["Priority"] = self.Priority
        result["ScriptLineNum"] = self.ScriptLineNum
        result["StartTime"] = self.StartTime
        result["LocalStartTime"] = self.LocalStartTime
        result["CommandType"] = self.CommandType
        result["Protocol"] = self.Protocol
        result["SourceName"] = Config.getHostname()
        result["SourceIP"] = Config.getHostIP()
        result["DestName"] = self.DestName
        result["DestIP"] = self.DestIP
        result["DestAddress"] = self.DestAddress
        result["NumOfTrials"] = self.NumOfTrials
        result["Success"] = self.Success
        result["reachedDest"] = self.reachedDest
        result["Exceptions"] = self.Exceptions
        result["RawDetails"] = self.RawDetails
        return result



class PingOperation(Operation):
    CommandType = "PING"
    def do(self):
        self._start()
        
        self.NumOfTrials = 4
        
        responses = []
        detail = {}
        
        for i in range (1,4):
            response = Ping.do_ping(self.DestIP, Config.config.getint("Performance", "ICMPTimeout"))
            if response is not None:
                responses.append(response)
                
        if len(responses) != 0:
            self.Success = True
            detail["sequence"] = 1
            detail["hopAddress"] = self.DestAddress
            detail["hopAddressStr"] = self.DestIP
            detail["hopNameStr"] = self.DestName
            detail["lostNum"] = 4 - len(responses)
            detail["bestTime"] = min(responses)
            detail["worstTime"] = max(responses)
            detail["avgTime"] = sum(responses) / float(len(responses))
            detail["returnTTL"] = 1
            detail["replyType"] = 0
            detail["errorCode"] = -1
            
        self.RawDetails["Detail"] = detail



class TracerouteOperation(Operation):
    CommandType = "TRACEROUTE"
    def do(self):
        #self._start()
        return True
    def getResult(self):
        return True
        