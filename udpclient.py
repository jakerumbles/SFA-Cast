# Networking Project
# Ruben, Emalee, Jake
# 
# This is the UDP Multicast Client 
# This establishes a UDP Multicast socket and connection#

# Libraries
import socket
from zlib import decompress
import sys
import os
import pygame
import threading
import datetime
import struct

SFACAST_GRP = '224.0.0.1'

# pathh() gets the pathname from SFACastGUICLIENT.py
def pathh():
    direct = os.path.expanduser('~/Desktop')
    newpath = direct + "/SFACAST-Screenshots"
    return newpath

# Takes the screenshot, names the screesnshot using the date and time and returns the new path
def screenshot_path():
    path = datetime.datetime.now().strftime('./screenshot/screenshot_%Y-%m-%d_%H_%M_%S.jpg')
    print("Screenshot saved as: %s" % path)
    return path

def buffer(conn, check):
    buf = b''
    while check != 0:
        data, addr = conn.recvfrom(4096)
        #print(len(data))
        buf += data
        check = check -1 
    return buf




def main(port=8080):
    # Initalize Pygame
    pygame.init()
    pygame.display.set_caption('SFA Cast')

    screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    watching = True    

    # Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    # bind YOUR IP address and port
    local = socket.gethostbyname(socket.gethostname())
    sock.bind((local, port))
    group = socket.inet_aton(SFACAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Receives Width 
    passed_w, addr = sock.recvfrom(4)
    w = int(str(passed_w, 'utf8'))
    print('received resolution width {} from {}'.format(w, addr))

    # Receives Height
    passed_h, addr = sock.recvfrom(4)
    h = int(str(passed_h, 'utf8'))
    print('received resolution height {} from {}'.format(h, addr))


    try:
        while watching:
            for event in pygame.event.get():
                # Resizes the window so that the feed is resized and not cut off
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Quit button breaks the Watching loop #
                if event.type == pygame.QUIT:
                    watching = False
                    break
                elif event.type == pygame.KEYDOWN :
                    # F12 calls the save screenshot function #
                    if event.key == pygame.K_F12:
                        pygame.image.save(pygame.display.get_surface(), screenshot_path())
                    # Escape key breaks the watching loop
                    # Useful for malfunctions #
                    if event.key == pygame.K_ESCAPE :
                        print("ESC key pressed. Closing Window.")
                        watching = False
                        break
            infoObj = pygame.display.Info()
            # Resolution
            WID = infoObj.current_w
            HGT = infoObj.current_h

            
            # Retreive the size of the pixels length, the pixels length and pixels
            s_len, addr = sock.recvfrom(1024)
            size_len = int(str(s_len, 'utf-8'))
            
            si, addr = sock.recvfrom(size_len*2)
            size = int(str(si,'utf-8'))

            # Recieve ending of while loop in buffer method
            ending, addr = sock.recvfrom(4)
            check = ending.decode('utf-8')
            check = int(check)

            pixels = buffer(sock, check)
            pixel = decompress(pixels)

            # Create the Surface from raw 
            img = pygame.image.fromstring(pixel, (w, h), 'RGB')
            dis = pygame.transform.smoothscale(img, (WID,HGT))

            # Display the picture
            screen.blit(dis, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    finally:
        print("Closing Connection")
        sock.close()


if __name__ == '__main__':
    main()