import Operation

class TracerouteOperation(Operation.Operation):
    CommandType = "TRACEROUTE"
    def do(self):
        #self._start()
        return True
    def getResult(self):
        return True