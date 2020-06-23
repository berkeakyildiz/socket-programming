import random
import socket


def send(packet, sock, addr, drop_prob):
    if random.random() > float(drop_prob):
        sock.sendto(packet, addr)
    return


def recv(sock):
    packet, addr = sock.recvfrom(1024)
    return packet, addr
