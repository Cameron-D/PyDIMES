from dimes import Script
from util import Log
    
script = Script.Script("default_script.xml")
script.execute()

script.operationQ.join()