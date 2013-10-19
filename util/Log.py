from datetime import datetime
from util import Config
import threading

displaylock = threading.Lock()
filelock = threading.Lock()

logfile = open('pydimes.log', 'a')

def log(message, verbosity = 0):
    """
    Logs a message to the console and a file.
    message = the message to print out
    verbosity = the level:
    0 - Debug
    1 - Information
    2 - Important
    """
    if Config.config.getint("Debug", "DisplayVerbosity") <= verbosity:
        global displaylock
        displaylock.acquire()
        print "%s: %s" % (str(datetime.now()).strip("0"), message)
        displaylock.release()
    if Config.config.getint("Debug", "LogVerbosity") <= verbosity:
        global filelock
        filelock.acquire()
        logfile.write("%s: %s\n" % (str(datetime.now()).strip("0"), message))
        logfile.flush()
        filelock.release()