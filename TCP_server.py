# Networking Project
# Ruben, Emalee, Jake
# 
# This is the TCP Server 
# This establishes a TCP socket and connection #

# Libraries
from threading import Thread
from zlib import compress
import socket
import os
from mss import mss
import pygame

# Initalize Pygame
pygame.init()

# Grabs the current screen resolution
infoObj = pygame.display.Info()
WID = infoObj.current_w # Width
HGT = infoObj.current_h # Height

def retreive_frame(conn):
    with mss() as sct:
        # The region that is needed to be captured - using the Width and Height defined
        monitor = {'top': 0, 'left': 0, 'width': WID, 'height': HGT}
        while 'capturing':
            # Capture the screen
            img = sct.grab(monitor)
            # Compression level. 1 being lowest, 9 being highest
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

def main(port=5000):
    '''
    Main method
    '''
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        local = socket.gethostbyname(socket.gethostname())
        sock.bind((local, port)) # Bind to group and host
        sock.listen(10) # Allows 10 machines to listen
    except OSError as e:
        print("****Likely the port was already in use.  Increment port by 1 and try again****")
        print("The error: " + str(e))
    try:
        print("listening on %s:%s" % (local, port))
        while 'connected':
            # Get connection and the address that you are sending to
            conn, addr = sock.accept() 
            # print('Client connected IP:', addr) # Check
            # Send the Width to the client servers #
            conn.send(str(WID).encode('utf-8'))
            # Send the Height to the client servers #
            conn.send(str(HGT).encode('utf-8')) 
            # threads the frames and starts the threads
            thread = Thread(target=retreive_frame, args=(conn,)) 
            thread.start()
    except:
        print("problem lol")
    finally:
        sock.close()


if __name__ == '__main__':
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    main()
    