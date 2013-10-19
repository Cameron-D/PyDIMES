import threading
from datetime import datetime

loglock = threading.Lock()

def log(message):
    global loglock
    loglock.acquire()
    print "%s: %s" % (str(datetime.now()).strip("0"), message)
    loglock.release()