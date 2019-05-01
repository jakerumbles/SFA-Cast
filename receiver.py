import socket
import struct
import sys
from zlib import decompress

SFACAST_GRP = '224.0.0.1'
SFACAST_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', SFACAST_PORT))

group = socket.inet_aton(SFACAST_GRP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#sock.setblocking(False)
#sock.setsockopt(socket.SOL_IP,socket.IP_ADD_MEMBERSHIP, socket.inet_aton(SFACAST_GRP)+socket.inet_aton("144.96.33.254"))

def recvall(conn, length):
    """ Retreive all pixels. """
    try:
        buf = conn.recv(length)
    except:
        return None
    
    return buf

passed_w, addr = sock.recvfrom(4)
w = int(str(passed_w, 'utf8'))
print('received resolution width {} from {}'.format(w, addr))


passed_h, addr = sock.recvfrom(4)
h = int(str(passed_h, 'utf8'))
print('received resolution height {} from {}'.format(h, addr))
# Receive/respond loop
while True:
    # Retreive the size of the pixels length, the pixels length and pixels
    s_len, addr = sock.recvfrom(1024)
    size_len = int(str(s_len, 'utf-8'))
    print(size_len)
    #si = int.from_bytes(sock.recvfrom(1024), byteorder='big')
    si, addr = sock.recvfrom(size_len*2)
    size = int(str(si,'utf-8'))
    print("image size in bytes: {}".format(size) )

    #pixels = decompress(recvall(sock, size*2))
