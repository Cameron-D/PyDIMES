from dimes import Script
from util import Log
from util import Config
import threading, time
    
script = Script.Script("default_script.xml")
script.execute()

try:
    while threading.active_count() > 1:
        time.sleep(0.1)
    Log.log("All done, exiting!", 3)
except KeyboardInterrupt:
    Log.log("Received Ctrl+C, ending %d threads... (This may take a moment)" % threading.active_count(), 3)