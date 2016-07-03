import socket
import sys
import suporte 

from struct import pack, unpack

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

if len(sys.argv)<2:
    print "Error: do something"
    sys.exit()
else:
    chaves, valores = suporte.lerArquivo(sys.argv[1])
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    
    data, address = sock.recvfrom(4096)    
    tipo, mensagem = unpack('!H20s', data)
    mensagem = mensagem.rstrip('\0')
    if tipo == 1:
        if mensagem in chaves:
            sent = sock.sendto(pack("!H100s",3, valores[chaves.index(mensagem)]), address)
        else: 
            sent = sock.sendto(pack("!H100s",3,"No encontrado"), address)

        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
