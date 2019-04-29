
# Projector Server

from threading import Thread
from zlib import compress
import socket
import os
from mss import mss
import cv2
import sys
import struct

import pygame
pygame.init()
infoObj = pygame.display.Info()
WID = infoObj.current_w
HGT = infoObj.current_h
def retreive_frame(conn):
    with mss() as sct:
        # The region to capture
        monitor = {'top': 0, 'left': 0, 'width': WID, 'height': HGT}
        # monitor = sct.monitors[0]
        while 'capturing':
            # Capture the screen
            img = sct.grab(monitor)
        
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 9)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            # Send the actual pixels length
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            # Send pixels
            conn.sendall(pixels)

def main():
    SFACAST_GROUP = '224.0.0.1'   # IP from Dr. Glendowne
    SFACAST_PORT = 8080         # High number port
    multicast_group = (SFACAST_GROUP, SFACAST_PORT)
    ttl = struct.pack('b', 2)           # Set time-to-live
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.settimeout(0.2)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        print('Server started.')

        while 'connected':
            #print('Client connected IP:', addr)
            sock.sendto(str(WID).encode('utf-8'), multicast_group)
            sock.sendto(str(HGT).encode('utf-8'), multicast_group)
            thread = Thread(target=retreive_frame, args=(sock,))
            thread.start()
    finally:
        sock.close()


if __name__ == '__main__':
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    main()
    