'''
Projector Server
'''
from threading import Thread
from zlib import compress
import socket
from mss import mss
import cv2
import pygame
import time

SFACAST_GROUP = '224.0.0.1'   # IP from Dr. Glendowne
SFACAST_PORT = 8080         # High number port
#MAX = 65535

pygame.init()
infoObj = pygame.display.Info()
WID = infoObj.current_w
HGT = infoObj.current_h
print(WID)
print(HGT)

def retreive_frame(conn):
    '''
    Use mss module to grab current frame
    '''
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
            print(size_len)
            conn.sendto(str(size_len).encode('utf-8'), (SFACAST_GROUP, SFACAST_PORT))

            # Send the actual pixels length
            size_bytes = str(size).encode('utf-8')
            conn.sendto(size_bytes, (SFACAST_GROUP, SFACAST_PORT))
            print(size_bytes.decode('utf-8'), "sent")
            
            # Send pixels
            min = 0
            max = 4096
            nump = int(size / 4096)
            nump = nump + 1
            ending = str(nump)
            
            check = nump
            while check != 0:
                runs = pixels[min:max]
                #conn.sendto(runs, (SFACAST_GROUP, SFACAST_PORT))
                min = min + 4096
                max = max + 4096
                check -=1
                #print("sent data")


            #conn.sendto(pixels, (SFACAST_GROUP, SFACAST_PORT))

def create_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton('144.96.33.117'))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    
    return sock

def main():
    '''
    Main method
    '''
    GRP = "224.0.0.1"
    PORT= 8080

    group = (GRP, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    #sock.bind((host, port))

    #sock.listen(1)
    try:
        print('Server started.')
        sock.sendto(str(WID).encode('utf-8'), group)
            #print(WID)
        sock.sendto(str(HGT).encode('utf-8'), group)
        while True: 
            #print(HGT)
           # print(sock.recvfrom(1024))
            #thread = Thread(target=retreive_frame, args=(sock,))
            retreive_frame(sock)
            #thread.start()
            #time.sleep(0.2)
    
    finally:
        sock.close()



if __name__ == '__main__':
    main()
    