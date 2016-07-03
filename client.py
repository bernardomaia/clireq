# A CHAVE TEM ATEH 20 BYTES
# O VALOR TEM ATEH 100 BYTES

import sys
from struct import pack, unpack, calcsize
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
        
        try:
            data, address = s.recvfrom(calcsize('!H100s'))
            tipo, corpo = unpack("!H100s", data)
            if (tipo == 3):
                print address,"respondeu:", corpo
        except socket.timeout:
            print "\nTimeout!!\n"