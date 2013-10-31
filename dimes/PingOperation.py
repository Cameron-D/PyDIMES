import time, socket, random, select, struct, Operation
from util import ICMP
from util import Config
from util import PacketSequence

class PingOperation(Operation.Operation):
    CommandType = "PING"
    def do(self):
        self._start()
        
        self.NumOfTrials = 4
        
        responses = []
        detail = {}
        
        for i in range (1,4):
            response = self.do_ping(self.DestIP, Config.config.getint("Performance", "ICMPTimeout"))
            if response is not None:
                responses.append(response)
                
        if len(responses) != 0:
            self.Success = True
            detail["sequence"] = 1
            detail["hopAddress"] = self.DestAddress
            detail["hopAddressStr"] = self.DestIP
            detail["hopNameStr"] = self.DestName
            detail["lostNum"] = 4 - len(responses)
            detail["bestTime"] = min(responses)
            detail["worstTime"] = max(responses)
            detail["avgTime"] = sum(responses) / float(len(responses))
            detail["returnTTL"] = 1
            detail["replyType"] = 0
            detail["errorCode"] = -1
            
        self.RawDetails["Detail"] = detail
        
    def do_ping(self, dest_addr, timeout=5):
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP.ICMP_CODE)
        except socket.error, (errno, msg):
            if errno in ICMP.ERROR_DESCR:
                # Operation not permitted
                raise socket.error(''.join((msg, ICMP.ERROR_DESCR[errno])))
            raise # raise the original error
        try:
            host = socket.gethostbyname(dest_addr)
        except socket.gaierror:
            return
        # Maximum for an unsigned short int c object counts to 65535 so
        # we have to sure that our packet id is not greater than that.
        packet_id = PacketSequence.getnext()
        packet = ICMP.create_packet(packet_id)
        while packet:
            # The icmp protocol does not use a port, but the function
            # below expects it, so we just give it a dummy port.
            sent = my_socket.sendto(packet, (dest_addr, 1))
            packet = packet[sent:]
        delay = self.receive_ping(my_socket, packet_id, time.time(), timeout)
        my_socket.close()
        return delay
    
    
    def receive_ping(self, my_socket, packet_id, time_sent, timeout):
        # Receive the ping from the socket.
        time_left = timeout
        while True:
            started_select = time.time()
            ready = select.select([my_socket], [], [], time_left)
            how_long_in_select = time.time() - started_select
            if ready[0] == []: # Timeout
                return
            time_received = time.time()
            rec_packet, addr = my_socket.recvfrom(1024)
            icmp_header = rec_packet[20:28]
            type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
            if p_id == packet_id:
                return time_received - time_sent
            time_left -= time_received - time_sent
            if time_left <= 0:
                return