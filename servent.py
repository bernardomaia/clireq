import socket
from struct import pack, unpack
import sys

from suporte import printDic, lerArquivo

if len(sys.argv) < 4:
    print "Error: do something"
    sys.exit()

SEQ_NO = 0
neighbors = []
history = []

ip, port = sys.argv[1].split(":")
port = int(port)
address = (ip, port)
inputFile = sys.argv[2]
for i in range (3, len(sys.argv)):
    ipN, portN = sys.argv[i].split(":")
    portN = int(portN)
    if (ipN,portN) not in neighbors:
        neighbors.append((ipN, portN))

# Create a UDP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
print 'starting up on %s port %s' % address
s.bind(address)

chaves, valores = lerArquivo(inputFile)

print "Vizinhos"
print neighbors
print "Dicionario"
printDic(chaves, valores)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = s.recvfrom(4096)
    tipo = int(unpack("!H",data[:2])[0])
    
    if (tipo == 1):
        print "CLIREQ"
        _,key = unpack("!H20s",data)
        key = key.rstrip('\0')
        if key in chaves:
            print "Eu tenho a chave", key
            s.sendto(pack("!H100s", 3, key+"\t"+valores[chaves.index(key)]), address)
        
        ip1, ip2, ip3, ip4 = address[0].split(".")
        ip1 = int(ip1)
        ip2 = int(ip2)
        ip3 = int(ip3)
        ip4 = int(ip4)
        portClient = address[1]
        for n in neighbors:
            print "Eu enviei para o vizinho", n
            s.sendto(pack("!HHBBBBHI20s",2,3,ip1, ip2, ip3, ip4, portClient, SEQ_NO, key), n)
        history.append((ip1, ip2, ip3, ip4, portClient, SEQ_NO, key))
        SEQ_NO += 1
            
    if (tipo == 2):
        print "QUERY"
        tipo, ttl, ip1, ip2, ip3, ip4, port, seqNo, key = unpack("!HHBBBBHI20s", data)
        if (ip1, ip2, ip3, ip4, port, seqNo, key) not in history:
            history.append((ip1, ip2, ip3, ip4, port, seqNo, key))
            key = key.rstrip('\0')
            if key in chaves:
                print "Eu tenho a chave", key
                ip = str(ip1)+"."+str(ip2)+"."+str(ip3)+"."+str(ip4)
                s.sendto(pack("!H100s", 3, key+"\t"+valores[chaves.index(key)]), (ip, port))
            if (ttl > 1):
                for n in neighbors:
                    if address != n:
                        print "Eu enviei para o vizinho", n
                        s.sendto(pack("!HHBBBBHI20s",tipo,ttl-1,ip1, ip2, ip3, ip4, port, seqNo, key), n)