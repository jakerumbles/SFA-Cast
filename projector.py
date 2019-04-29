# Authors: Jake Edwards, Emalee Keesler, and Ruben Orozco
# Date: 3/19/2019
# Class: CSC 435-001
# Project: SFA-Cast

#Libraries
import socket
import sys
import struct

#UDP Multicasting Variables
SFACAST_GROUP = '224.0.0.1'   # IP from Dr. Glendowne
SFACAST_PORT = 8080         # High number port
multicast_group = (SFACAST_GROUP, SFACAST_PORT)
ttl = struct.pack('b', 2)           # Set time-to-live
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.settimeout(0.2)
sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(MCAST_IF_IP))
message = b'very important data'


try:

    # Send data to the multicast group
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, multicast_group)


    # Look for responses from all recipients
    while True:
        print('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print('received {!r} from {}'.format(data, server))

finally:
    print('closing socket')
    sock.close()


