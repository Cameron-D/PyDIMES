import threading, time
import Script
from util import Log

class Worker(threading.Thread):
    operation = None
    def __init__(self, script):
        threading.Thread.__init__(self)
        assert isinstance(script, Script.Script)
        self.script = script
        Log.log("Thread is %s, script is %s" % (self.name, self.script.id)) 
    def run(self):
        Log.log("%s starting" % self.name)
        while(not self.script.operationQ.empty()):
            self.script.operationQlock.acquire()
            Log.log("%s got lock" % self.name)
            operation = self.script.operationQ.get()
            Log.log("%s got item" % self.name)
            self.script.operationQlock.release()
            Log.log("%s released lock" % self.name)
            
            operation.do()
            Log.log("%s executed" % self.name)
            