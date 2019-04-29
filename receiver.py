import socket
import struct
import sys

SFACAST_GRP = '224.0.0.1'
SFACAST_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SFACAST_GRP, SFACAST_PORT))
group = socket.inet_aton(SFACAST_GRP)
mreq = struct.pack('4s4s', group, socket.inet_aton(group))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    print('received {} bytes from {}'.format(
        len(data), address))
    print(data)
