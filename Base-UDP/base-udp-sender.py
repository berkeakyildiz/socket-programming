import socket
import sys
import time

import baseudppacket as packet
import baseudpudt as udt

PACKET_SIZE = 1024
RECEIVER_ADDR = ('localhost', 9502)
SENDER_ADDR = ('localhost', 9501)
SLEEP_INTERVAL = 0.05


def send(sock, filename, drop_prob):
    try:
        file = open(filename, 'rb')
    except IOError:
        print('Unable to open', filename)
        return

    packets = []
    while True:
        data = file.read(PACKET_SIZE)
        if not data:
            break
        packets.append(packet.make_datagram(data))

    file.close()
    next_to_send = 0

    start_time = time.time()
    while True:
        if next_to_send < len(packets):
            udt.send(packets[next_to_send], sock, RECEIVER_ADDR, drop_prob)
            time.sleep(SLEEP_INTERVAL)
            next_to_send += 1
            print("sent: " + str(next_to_send))
        else:
            break
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    if len(sys.argv) != 3:
        print('Expected filename and drop_probability as command line argument')
        exit()
    filename = sys.argv[1]
    drop_prob = sys.argv[2]
    print("READY TO SEND")
    send(sock, filename, drop_prob)
    sock.close()
