import threading

loglock = threading.Lock()

def log(message):
    global loglock
    loglock.acquire()
    print message
    loglock.release()