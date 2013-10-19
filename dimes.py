from dimes import Script
from util import Log
import threading
import time
    
script = Script.Script("default_script.xml")
script.execute()

try:
    while threading.active_count() > 0:
        time.sleep(0.1)
except KeyboardInterrupt:
    Log.log("Received Ctrl+C, ending %d threads... (This may take a moment)" % threading.active_count())