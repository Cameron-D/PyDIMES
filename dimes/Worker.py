import threading, time
import Script
from util import Log

class Worker(threading.Thread):
    operation = None
    def __init__(self, script):
        threading.Thread.__init__(self)
        self.script = script
        Log.log("Thread is %s, script is %s" % (self.name, self.script.id))

    def run(self):
        while(not self.script.operationQ.empty()):
            # Fetch an operation from the queue
            self.script.operationQlock.acquire()
            operation = self.script.operationQ.get()
            self.script.operationQlock.release()
            operation.do()
            self.script.operationQlock.acquire()
            operation = self.script.operationQ.task_done()
            self.script.operationQlock.release()