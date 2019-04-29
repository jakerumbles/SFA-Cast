import socket
from zlib import decompress
import sys
import os
import pygame
import threading
import datetime
import struct

def pathh():
    direct = os.path.expanduser('~/Desktop')
    newpath = direct + "/SFACAST-Screenshots"
    return newpath

def screenshot_path():
    path = datetime.datetime.now().strftime('./screenshot/screenshot_%Y-%m-%d_%H_%M_%S.jpg')
    print("Screenshot saved as: %s" % path)
    return path


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recvfrom(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main():
    SFACAST_GRP = '224.0.0.1'
    SFACAST_PORT = 8080

    pygame.init()
    pygame.display.set_caption('SFA Cast')
    infoObj = pygame.display.Info()
    WID = infoObj.current_w
    HGT = infoObj.current_h
    screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    watching = True    

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        sock.bind(('', SFACAST_PORT))
    else:
        sock.bind((SFAAST_GRP, SFACAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(SFACAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    passed_w = sock.recvfrom(4)
    w = int(str(passed_w, 'utf8'))
    print(w)

    passed_h = sock.recvfrom(4)
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
            size_len = int.from_bytes(sock.recvfrom(1), byteorder='big')
            size = int.from_bytes(sock.recvfrom(size_len), byteorder='big')
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