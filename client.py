###################################################
#            TP3: P2P key-value storage           #
#        Bernardo Maia e Fabricio Ferreira        #
#              Julho de 2016 - UFMG               #
###################################################

import sys
from struct import pack, unpack
import socket
import atexit

def exit(s):
    s.close()

if len(sys.argv) < 2:
    print "Error: inform a valid servent address!"
else:
    ip, port = sys.argv[1].split(":")
    address = (ip, int(port))
    print 'Servent at', address
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(4)
    atexit.register(exit, s)
    while True:
        key = raw_input("Type the key to seach: ")
        
        # send <CLIREQ (2 bytes), key (20 bytes)>
        s.sendto(pack('!H20s', 1, key), address)
        stop = False
        retransmitted = False
        while (not stop):
            if retransmitted:
                print "Retransmitting..."
            try:
                while True:
                    dataResponse, addressResponse = s.recvfrom(4096)
                    tipo, corpo = unpack("!H121s", dataResponse)
                    if (tipo == 3):
                        print addressResponse,"respondeu:", corpo
                        stop = True
            except socket.timeout:
                print "\nTimeout!!\n"
                if retransmitted:
                    stop = True
                retransmitted = not retransmitted
