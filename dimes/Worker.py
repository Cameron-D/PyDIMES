from util import Log
import threading, time, Script


class Worker(threading.Thread):
    operation = None
    def __init__(self, script):
        threading.Thread.__init__(self)
        self.script = script
        Log.log("Thread is %s, script is %s" % (self.name, self.script.id))

    def run(self):
        while(not self.script.operationQ.empty()):
            # Fetch an operation from the queue
            operation = self.script.operationQ.get()
            
            # Execute it!
            result = operation.do()
            
            # Add it onto the result queue
            
            # Mark it as complete
            operation = self.script.operationQ.task_done()
        return