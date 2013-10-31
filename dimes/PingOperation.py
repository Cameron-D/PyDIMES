import Operation
from util import Ping
from util import Config

class PingOperation(Operation.Operation):
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