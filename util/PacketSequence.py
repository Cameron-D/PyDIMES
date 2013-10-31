import threading

sequencelock = threading.Lock()
sequence = 0

def next():
    """
    Gets the next number in the sequence, used for identifying packets
    """
    sequencelock.acquire()
    if(sequence == 65534): # 65535 is the maximum ID supported, leave some room
        sequence = 0
        
    sequence = sequence + 1
    nextseq = sequence
    
    sequencelock.release()
    
    return nextseq