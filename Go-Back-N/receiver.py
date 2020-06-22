# receiver.py - The receiver in the reliable data transer protocol
import socket
import time

import packet
import udt

RECEIVER_ADDR = ('localhost', 8080)


# Receive packets from the sender
def receive(sock, filename):
    # Open the file for writing
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return

    expected_num = 0
    while True:
        # Get the next packet from the sender
        pkt, addr = udt.recv(sock)
        if not pkt:
            break
        seq_num, data = packet.extract(pkt)
        print('Got packet', seq_num)

        # Send back an ACK
        if seq_num == expected_num:
            print('Got expected packet')
            print('Sending ACK', expected_num)
            pkt = packet.make(expected_num)
            udt.send(pkt, sock, addr)
            expected_num += 1
            file.write(data)
        else:
            print('Sending ACK', expected_num - 1)
            pkt = packet.make(expected_num - 1)
            udt.send(pkt, sock, addr)

    file.close()


# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    filename = "../received-data/received_small_data.txt"
    start_time = time.time()
    receive(sock, filename)
    sock.close()
    print("--- %s seconds ---" % (time.time() - start_time))
