import socket

SFACAST_GRP = '224.0.0.1'
SFACAST_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((SFACAST_GRP, SFACAST_PORT))
# print("Socket Created.") #Checker