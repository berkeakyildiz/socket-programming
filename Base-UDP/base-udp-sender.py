import socket
import sys
import time

import baseudppacket as packet
import baseudpudt as udt

PACKET_SIZE = 1024
RECEIVER_ADDR = ('localhost', 8080)
SENDER_ADDR = ('localhost', 0)
SLEEP_INTERVAL = 0.05


# Send thread
def send(sock, filename):
    # Open the file
    try:
        file = open(filename, 'rb')
    except IOError:
        print('Unable to open', filename)
        return

    # Add all the packets to the buffer
    packets = []
    while True:
        data = file.read(PACKET_SIZE)
        if not data:
            break
        packets.append(packet.make_datagram(data))

    # Send empty packet as sentinel
    udt.send(packet.make_empty(), sock, RECEIVER_ADDR)
    file.close()
    next_to_send = 0

    while True:
        udt.send(packets[next_to_send], sock, RECEIVER_ADDR)
        time.sleep(SLEEP_INTERVAL)
        next_to_send += 1
        print("sent: " + str(next_to_send))


# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    # if len(sys.argv) != 2:
    #     print('Expected filename as command line argument')
    #     exit()
    # filename = sys.argv[1]
    filename = "/home/bakyildiz/PycharmProjects/socket-programming/data/small-data.txt"
    start_time = time.time()
    print("READY TO SEND")
    send(sock, filename)
    sock.close()
    print("--- %s seconds ---" % (time.time() - start_time))
