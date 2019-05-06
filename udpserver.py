# Networking Project
# Ruben, Emalee, Jake
# 
# This is the UDP Multicast Server 
# This establishes a UDP Multicast socket and connection#

# Libraries 
from threading import Thread
from zlib import compress
import socket
from mss import mss
import pygame

SFACAST_GROUP = '224.0.0.1'   # IP from Dr. Glendowne
SFACAST_PORT = 8080         # High number port

# Initalize Pygame
# Grab current screen resolution for capture region
pygame.init()
infoObj = pygame.display.Info()
WID = infoObj.current_w # Width
HGT = infoObj.current_h # Height


def retreive_frame(conn):
    with mss() as sct:
        # The region to capture
        monitor = {'top': 0, 'left': 0, 'width': WID, 'height': HGT}

        while 'capturing':
            # Capture the screen
            img = sct.grab(monitor)
            
            # Tweak the compression level here (0-9)
            pixels = compress(img.rgb, 9)

            # Send the size of the pixels length
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            #print(size_len)
            conn.sendto(str(size_len).encode('utf-8'), (SFACAST_GROUP, SFACAST_PORT))

            # Send the actual pixels length
            size_bytes = str(size).encode('utf-8')
            conn.sendto(size_bytes, (SFACAST_GROUP, SFACAST_PORT))
            
            # Send pixels
            min = 0
            max = 4096
            s_b = int(size_bytes.decode('utf-8'))
            nump = int( s_b / max)
            nump = nump + 1
            ending = str(nump).encode('utf-8')
            conn.sendto(ending, (SFACAST_GROUP, SFACAST_PORT))

            check = nump
            while check != 0:
                runs = pixels[min:max]
                conn.sendto(runs, (SFACAST_GROUP, SFACAST_PORT))
                min = min + 4096
                max = max + 4096
                check -=1

def main(port=5000):
    group = (SFACAST_GROUP, SFACAST_PORT)
    # Create socket object 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.sendto(str(WID).encode('utf-8'), group) # Send Width
        sock.sendto(str(HGT).encode('utf-8'), group) # Send Height
        while True: 
            retreive_frame(sock)
    finally:
        sock.close()

if __name__ == '__main__':
    main()
    