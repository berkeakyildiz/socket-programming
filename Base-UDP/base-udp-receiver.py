import socket
import time
import sys

import baseudppacket as packet
import baseudpudt as udt

RECEIVER_ADDR = ('localhost', 9502)


def receive(sock, filename):
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return
    pkt_count = 0
    start_time = time.time()
    while True:
        pkt, addr = udt.recv(sock)
        if pkt_count == 0:
            start_time = time.time()
            print("Start time: " + str(start_time))
        if pkt:
            data = packet.extract_datagram(pkt)
            file.write(data)
            pkt_count += 1
            print("received: " + str(pkt_count))

            print("--- %s seconds ---" % (time.time() - start_time))
        else:
            break
    file.close()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()
    # filename = sys.argv[1]
    filename = "/home/bakyildiz/PycharmProjects/socket-programming/received-data/received_small_data.txt"
    print("READY TO RECEIVE")
    receive(sock, filename)
    sock.close()
