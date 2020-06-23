import _thread
import socket
import time
import sys

import packet
import udt
from timer import Timer

PACKET_SIZE = 1024
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 0)
SLEEP_INTERVAL = 0.05
TIMEOUT_INTERVAL = 0.5
WINDOW_SIZE = 4

base = 0
mutex = _thread.allocate_lock()
send_timer = Timer(TIMEOUT_INTERVAL)


def set_window_size(num_packets):
    global base
    return min(WINDOW_SIZE, num_packets - base)


def send(sock, filename, drop_prob):
    global mutex
    global base
    global send_timer

    try:
        file = open(filename, 'rb')
    except IOError:
        print('Unable to open', filename)
        return

    packets = []
    seq_num = 0
    while True:
        data = file.read(PACKET_SIZE)
        if not data:
            break
        packets.append(packet.make(seq_num, data))
        seq_num += 1

    num_packets = len(packets)
    print('I gots', num_packets)
    window_size = set_window_size(num_packets)
    next_to_send = 0
    base = 0

    _thread.start_new_thread(receive, (sock,))

    while base < num_packets:
        mutex.acquire()
        while next_to_send < base + window_size:
            print('Sending packet', next_to_send)
            udt.send(packets[next_to_send], sock, RECEIVER_ADDR, drop_prob)
            next_to_send += 1

        if not send_timer.running():
            print('Starting timer')
            send_timer.start()

        while send_timer.running() and not send_timer.timeout():
            mutex.release()
            print('Sleeping')
            time.sleep(SLEEP_INTERVAL)
            mutex.acquire()

        if send_timer.timeout():
            print('Timeout')
            send_timer.stop()
            next_to_send = base
        else:
            print('Shifting window')
            window_size = set_window_size(num_packets)
        mutex.release()

    udt.send(packet.make_empty(), sock, RECEIVER_ADDR, drop_prob)
    file.close()


def receive(sock):
    global mutex
    global base
    global send_timer

    while True:
        pkt, _ = udt.recv(sock)
        ack, _ = packet.extract(pkt)

        print('Got ACK', ack)
        if ack >= base:
            mutex.acquire()
            base = ack + 1
            send_timer.stop()
            mutex.release()


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    # if len(sys.argv) != 3:
    #     print('Expected filename, drop_prob and window_size as command line argument')
    #     exit()
    # filename = sys.argv[1]
    # drop_prob = sys.argv[2]
    # WINDOW_SIZE = sys.argv[3]
    WINDOW_SIZE = 8
    filename = "../data/medium-data.txt"
    drop_prob = 0.004
    start_time = time.time()
    send(sock, filename, drop_prob)
    sock.close()
    print("--- %s seconds ---" % (time.time() - start_time))

