import ConfigParser, platform, socket, time

"""Handles processing of config file and other agent-specific bits of data"""

config = ConfigParser.ConfigParser()
config.read("settings.ini")

_hostname = platform.node()
if _hostname == "":
    _hostname = config["Agent"]["Name"]
_ip = None
_lastIP = 0
    
def getHostname():
    return _hostname

def getHostIP():
    # Get the IP again every 5 mins (For dynamic IPs/DHCP/changing network, etc.)
    if time.time() - _lastIP > 300:
        # http://stackoverflow.com/a/1267524
        _ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
        _now = time.time()
    return _ip