import socket
from zlib import decompress
import sys
import os
import pygame
import threading
import datetime
import struct


SFACAST_GRP = '224.0.0.1'


def pathh():
    direct = os.path.expanduser('~/Desktop')
    newpath = direct + "/SFACAST-Screenshots"
    return newpath

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




def main(host='224.0.0.1', port=8080):
    pygame.init()
    pygame.display.set_caption('SFA Cast')
    infoObj = pygame.display.Info()
    WID = infoObj.current_w
    HGT = infoObj.current_h
    screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    watching = True    

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('', port))

    group = socket.inet_aton(SFACAST_GRP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    passed_w, addr = sock.recvfrom(4)
    w = int(str(passed_w, 'utf8'))
    print('received resolution width {} from {}'.format(w, addr))


    passed_h, addr = sock.recvfrom(4)
    h = int(str(passed_h, 'utf8'))
    print('received resolution height {} from {}'.format(h, addr))


    try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == pygame.QUIT:
                    watching = False
                    break
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_F12:
                        pygame.image.save(pygame.display.get_surface(), screenshot_path())
                    if event.key == pygame.K_ESCAPE :
                        print("ESC key pressed. Closing Window.")
                        watching = False
                        break
            infoObj = pygame.display.Info()
            WID = infoObj.current_w
            HGT = infoObj.current_h

            
            # Retreive the size of the pixels length, the pixels length and pixels
            s_len, addr = sock.recvfrom(1024)
            size_len = int(str(s_len, 'utf-8'))
            #print(size_len)

            #si = int.from_bytes(sock.recvfrom(1024), byteorder='big')
            si, addr = sock.recvfrom(size_len*2)
            size = int(str(si,'utf-8'))
            #print(size)

            ending, addr = sock.recvfrom(4)
            check = ending.decode('utf-8')
            check = int(check)
            #print("ending {}".format(check))

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