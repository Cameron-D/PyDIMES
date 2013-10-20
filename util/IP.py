import socket, struct

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def reverseDNS(addr):
    try:
        return socket.gethostbyaddr(addr)[0]
    except socket.herror:
        return addr