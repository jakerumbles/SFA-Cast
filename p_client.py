import socket
from zlib import decompress

import os
import pygame

WIDTH = 1920
HEIGHT = 1080


def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host='144.96.63.85', port=5000):
    pygame.init()
    pygame.display.set_caption('SFA Cast')
    infoObj = pygame.display.Info()
    WID = infoObj.current_w
    HGT = infoObj.current_h
    screen = pygame.display.set_mode((WID, HGT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    watching = True    

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
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

            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (WID, HGT), 'RGB')

            img = pygame.transform.scale(img, (WID, HGT))

            # Display the picture
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
    finally:
        print("Closing Connection")
        sock.close()


if __name__ == '__main__':
    main()