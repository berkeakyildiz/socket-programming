import socket
import time
import sys

import selectiverepeatpacket as packet
import selectiverepeatudt as udt

RECEIVER_ADDR = ('localhost', 8080)


def receive(sock, filename, drop_prob):
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return

    expected_num = 0
    while True:
        pkt, addr = udt.recv(sock)
        if not pkt:
            break
        seq_num, data = packet.extract(pkt)
        print('Got packet', seq_num)

        if seq_num == expected_num:
            print('Sending ACK', expected_num)
            pkt = packet.make(expected_num)
            udt.send(pkt, sock, addr, drop_prob)
            expected_num += 1
            file.write(data)
        else:
            print('Sending ACK', expected_num - 1)
            pkt = packet.make(expected_num - 1)
            udt.send(pkt, sock, addr, drop_prob)

    file.close()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    if len(sys.argv) != 3:
        print('Expected filename, drop_prob as command line argument')
        exit()
    filename = sys.argv[1]
    drop_prob = sys.argv[2]
    start_time = time.time()
    receive(sock, filename, drop_prob)
    sock.close()
    print("---Download time: %s seconds ---" % (time.time() - start_time))