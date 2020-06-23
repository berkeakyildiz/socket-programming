import random
import socket

DROP_PROB = 9


def send(packet, sock, addr):
    if random.randint(0, DROP_PROB) > 0:
        sock.sendto(packet, addr)
    return


def recv(sock):
    packet, addr = sock.recvfrom(1024)
    return packet, addr
