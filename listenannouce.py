import sys
import re
import socket
import time
import struct


def ip_is_local(ip_string):
    combined_regex = "(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^192\.168\.)"
    return re.match(combined_regex, ip_string) is not None # is not None is just a sneaky way of converting to a boolean


def get_local_ip():

    # socket.getaddrinfo returns a bunch of info, so we just get the IPs it returns with this list comprehension.
    local_ips = [ x[4][0] for x in socket.getaddrinfo(socket.gethostname(), 80)
                  if ip_is_local(x[4][0]) ]

    # select the first IP, if there is one.
    local_ip = local_ips[0] if len(local_ips) > 0 else None

    # If the previous method didn't find anything, use this less desirable method that lets your OS figure out which
    # interface to use.
    if not local_ip:
        # create a standard UDP socket ( SOCK_DGRAM is UDP, SOCK_STREAM is TCP )
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Open a connection to one of Google's DNS servers. Preferably change this to a server in your control.
            temp_socket.connect(('8.8.8.8', 9))
            # Get the interface used by the socket.
            local_ip = temp_socket.getsockname()[0]
        except socket.error:
            # Only return 127.0.0.1 if nothing else has been found.
            local_ip = "127.0.0.1"
        finally:
            # Always dispose of sockets when you're done!
            temp_socket.close()
    return local_ip

def create_socket(multicast_ip, port):

    local_ip = get_local_ip()

    # create a UDP socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # allow reuse of addresses
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # set multicast interface to local_ip
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))

    # Set multicast time-to-live to 2...should keep our multicast packets from escaping the local network
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Construct a membership request...tells router what multicast group we want to subscribe to
    membership_request = socket.inet_aton(multicast_ip) + socket.inet_aton(local_ip)


    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership_request)


    if sys.platform.startswith("darwin"):
        my_socket.bind(('0.0.0.0', port))
    else:
        my_socket.bind((local_ip, port))

    return my_socket

def get_bound_multicast_interface(my_socket):

    response = my_socket.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF)
    socket.inet_ntoa(struct.pack('i', response))

def drop_multicast_membership(my_socket, multicast_ip):

    local_ip = get_local_ip()

    # Must reconstruct the same request used when adding the membership initially
    membership_request = socket.inet_aton(multicast_ip) + socket.inet_aton(local_ip)

    # Leave group
    my_socket.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, membership_request)

def listen_loop(multicast_ip, port):
    my_socket = create_socket(multicast_ip, port)

    while True:

        data, address = my_socket.recvfrom(4096)
        print("%s says the time is %s" % (address, data))

def announce_loop(multicast_ip, port):
    # Offset the port by one so that we can send and receive on the same machine
    my_socket = create_socket(multicast_ip, port + 1)

    while True:
        # Just sending Unix time as a message
        message = str(time.time())

        # Send data. Destination must be a tuple containing the ip and port.
        my_socket.sendto(message, (multicast_ip, port))
        time.sleep(1)


if __name__ == '__main__':

    multicast_address = "239.255.4.3"
    multicast_port = 1234

    # When launching this example, you can choose to put it in listen or announce mode.
    # Announcing doesn't require binding to a port, but we do it here just to reuse code.
    # It binds to the requested port + 1, allowing you to run the announce and listen modes
    # on the same machine at the same time.

    # In a real case, you'll most likely send and receive from the same port using Gevent or Twisted,
    # so the code in create_socket() will apply more directly.

    if sys.argv[1] == "listen":
        listen_loop(multicast_address, multicast_port)
    elif sys.argv[1] == "announce":
        announce_loop(multicast_address, multicast_port)
    else:
        exit("Run 'multicast_example.py listen' or 'multicast_example.py announce'.")
    