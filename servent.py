###################################################
#            TP3: P2P key-value storage           #
#        Bernardo Maia e Fabricio Ferreira        #
#              Julho de 2016 - UFMG               #
###################################################

import atexit
import socket
from struct import pack, unpack
import sys

from suporte import printDic, readInputFile


# close the socket before exiting
def exit(s):
    s.close()

# requires at lest 3 arguments, besides filename
if len(sys.argv) < 4 or len(sys.argv) > 13:
    print "Error: wrong number of arguments!"
    sys.exit()

SEQ_NO = 0

# stores the (ip:port) of neighbors
NEIGHBORS = []

# stores the history of messages received
HISTORY = []

# key-value dictionary
KEYS = []
VALUES = []

ip, port = sys.argv[1].split(":")
port = int(port)
myAddress = (ip, port)

# input file with the key-value list
inputFile = sys.argv[2]
KEYS, VALUES = readInputFile(inputFile)

# append all neighbors
for i in range (3, len(sys.argv)):
    ipN, portN = sys.argv[i].split(":")
    portN = int(portN)
    if (ipN,portN) not in NEIGHBORS and (ipN,portN) != myAddress:
        NEIGHBORS.append((ipN, portN))

# create an UDP/IP socket and bind it to the port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(myAddress)

# register at exit function
atexit.register(exit, s)

# print "Vizinhos"
# print neighbors
# print "Dicionario"
# printDic(KEYS, VALUES)

while True:
#     print HISTORY
#     print >>sys.stderr, '\nwaiting to receive message'
    data, addressSender = s.recvfrom(4096)
    tipo = int(unpack("!H",data[:2])[0])
    
    # CLIREQ: create a query and send it to all neighbors
    if (tipo == 1):
#         print "CLIREQ"
        tipo, key = unpack("!H20s",data)
        key = key.rstrip('\0')
        if key in KEYS:
#             print "Eu tenho a chave", key
            s.sendto(pack("!H121s", 3, key+"\t"+VALUES[KEYS.index(key)]), addressSender)
        
        # it was necessary to isolate each ip part to pack each into 1 byte value
        ip1, ip2, ip3, ip4 = addressSender[0].split(".")
        ip1 = int(ip1)
        ip2 = int(ip2)
        ip3 = int(ip3)
        ip4 = int(ip4)
        portClient = addressSender[1]
        
        for n in NEIGHBORS:
#             print "Eu enviei para o vizinho", n
            s.sendto(pack("!HHBBBBHI20s",2,3,ip1, ip2, ip3, ip4, portClient, SEQ_NO, key), n)
        
        HISTORY.append((ip1, ip2, ip3, ip4, portClient, SEQ_NO, key))
        SEQ_NO += 1
    
    # QUERY: test if it has the key-value and send query to all other neighbors        
    if (tipo == 2):
#         print "QUERY"
        tipo, ttl, ip1, ip2, ip3, ip4, port, seqNo, key = unpack("!HHBBBBHI20s", data)
        key = key.rstrip('\0')
        
        # have I received this query before?
        if (ip1, ip2, ip3, ip4, port, seqNo, key) not in HISTORY:
            HISTORY.append((ip1, ip2, ip3, ip4, port, seqNo, key))
            
            # send RESPONSE if I have it
            if key in KEYS:
#                 print "Eu tenho a chave", key
                ip = str(ip1)+"."+str(ip2)+"."+str(ip3)+"."+str(ip4)
                s.sendto(pack("!H121s", 3, key+"\t"+VALUES[KEYS.index(key)]), (ip, port))
            
            # share with neighbors
            if (ttl > 1):
                for n in NEIGHBORS:
                    if addressSender != n:
#                         print "Eu enviei para o vizinho", n
                        s.sendto(pack("!HHBBBBHI20s", tipo,ttl-1,ip1, ip2, ip3, ip4, port, seqNo, key), n)
#         else:
#             print "Ja tenho essa mensagem no historico"