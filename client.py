###################################################
#            TP3: P2P key-value store             #
#        Bernardo Maia e Fabricio Ferreira        #
#              Julho de 2016 - UFMG               #
###################################################

import atexit
import socket
from struct import pack, unpack
import sys


# close the socket before exiting
def exitFunction(s):
    s.close()

# requires at lest 1 argument, besides filename
if len(sys.argv) < 2:
    print "Error: inform a valid servent address!"
    sys.exit()

ip, port = sys.argv[1].split(":")
serventAddress = (ip, int(port))
# print 'Servent at', serventAddress

# create socket and set timeout as 4 seconds
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(4)

# register the exit function
atexit.register(exitFunction, s)

while True:
    key = raw_input("Type the key to search: ")
    
    # send <CLIREQ (2 bytes), key (20 bytes)>
    s.sendto(pack('!H20s', 1, key), serventAddress)
    
    stopSending = False
    retransmitted = False
    
    while (not stopSending):
        
        if retransmitted:
            print "Retransmitting..."
            s.sendto(pack('!H20s', 1, key), serventAddress)
        
        try:
            # receive responses
            while True:
                dataResponse, addressResponse = s.recvfrom(4096)
                tipo, data = unpack("!H121s", dataResponse)
                if (tipo == 3):
                    print addressResponse,"has it:", data
                    stopSending = True
        
        except socket.timeout:
            print "\nTimeout!!\n"
            if retransmitted:
                stopSending = True
            retransmitted = not retransmitted
