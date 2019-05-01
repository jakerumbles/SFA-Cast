# Networking Project
# Ruben, Emalee, Jake
# 
# This is the TCP Client 
# This establishes a TCP socket and connection#

import socket
from zlib import decompress
import sys
import os
import pygame
import threading
import datetime
from SFACastGUICLIENT import pathname

def pathh():
    direct = pathname
    newpath = direct + "/SFACAST-Screenshots"
    return newpath

def screenshot_path():
    path = datetime.datetime.now().strftime(pathname() + '/screenshot_%Y-%m-%d_%H_%M_%S.jpg')
    print("Screenshot saved as: %s" % path)
    return path


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host='144.96.63.57', port=5006):
    pygame.init()
    pygame.display.set_caption('SFA Cast')
    infoObj = pygame.display.Info()
    WID = infoObj.current_w
    HGT = infoObj.current_h
    screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    watching = True    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    passed_w = sock.recv(4)
    w = int(str(passed_w, 'utf8'))
    print(w)

    passed_h = sock.recv(4)
    h = int(str(passed_h, 'utf8'))
    print(h)

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
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            pixels = decompress(recvall(sock, size))

            # Create the Surface from raw 
            img = pygame.image.fromstring(pixels, (w, h), 'RGB')

            dis = pygame.transform.smoothscale(img, (WID,HGT))
            # Display the picture
            screen.blit(dis, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    finally:
        print("Closing Connection")
        sock.close()


if __name__ == '__main__':
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    main()