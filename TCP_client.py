# Networking Project
# Ruben, Emalee, Jake
# 
# This is the TCP Client 
# This establishes a TCP socket and connection#

# Libraries
import socket
from zlib import decompress
import sys
import os
import pygame
import threading
import datetime
from SFACastGUICLIENT import pathname

# pathh() gets the pathname from SFACastGUICLIENT.py
def pathh():
    direct = pathname
    return direct

# Takes the screenshot, names the screesnshot using the date and time and returns the new path
def screenshot_path():
    path = datetime.datetime.now().strftime(pathname() + '/screenshot_%Y-%m-%d_%H_%M_%S.jpg')
    # print("Screenshot saved as: %s" % path)
    return path


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host='192.168.1.8', port=5000):

    try:
        #Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except ConnectionRefusedError:
        print("Server is not broadcasting...exiting program")
        sys.exit(1)

    pygame.init()
    pygame.display.set_caption('SFA Cast')
    
    # Initialize pygame window to 1600x900.
    screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    watching = True    

    # Receives Width 
    passed_w = sock.recv(4)
    w = int(str(passed_w, 'utf8'))
    print(w)

    # Receives Height
    passed_h = sock.recv(4)
    h = int(str(passed_h, 'utf8'))
    print(h)

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
                    if event.key == pygame.K_S:
                        pygame.image.save(pygame.display.get_surface(), screenshot_path())
                    # Escape key breaks the watching loop
                    # Useful for malfunctions #
                    if event.key == pygame.K_ESCAPE :
                        print("ESC key pressed. Closing Window.")
                        watching = False
                        break
            infoObj = pygame.display.Info()
            # Client Resolution
            WID = infoObj.current_w
            HGT = infoObj.current_h

            # Retreive the size of the pixels length, the pixels length and pixels
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            pixels = decompress(recvall(sock, size))

            # Create the Surface from raw 
            img = pygame.image.fromstring(pixels, (w, h), 'RGB')

            # Scale surface to fit into resized window
            dis = pygame.transform.smoothscale(img, (WID,HGT))

            # Display the picture
            screen.blit(dis, (0, 0))
            pygame.display.flip()
            # Max Framerate
            clock.tick(60)
    finally:
        # Close socket when stream window is closed
        print("Closing Connection")
        sock.close()


if __name__ == '__main__':
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    main()