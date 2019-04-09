'''
Projector Server
'''
from threading import Thread
from zlib import compress
import socket
from mss import mss
import cv2
#import numpy

WIDTH = 1920
HEIGHT = 1080

def retreive_frame(conn):
    '''
    Use mss module to grab current frame
    '''
    with mss() as sct:
        # The region to capture
        monitor = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
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

def main(host='144.96.63.138', port=5000):
    '''
    Main method
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))

    sock.listen(1)
    try:
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=retreive_frame, args=(conn,))
            thread.start()
    finally:
        sock.close()


if __name__ == '__main__':
    main()
    