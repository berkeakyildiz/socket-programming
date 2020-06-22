import socket
import time

import baseudppacket as packet
import baseudpudt as udt

RECEIVER_ADDR = ('localhost', 8080)


# Receive packets from the sender
def receive(sock, filename):
    # Open the file for writing
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return

    while True:
        # Get the next packet from the sender
        pkt, addr = udt.recv(sock)
        if not pkt:
            break
        data = packet.extract_datagram(pkt)
        file.write(data)
    file.close()


# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR)
    filename = "/home/bakyildiz/PycharmProjects/socket-programming/received-data/received_small_data.txt"
    start_time = time.time()
    print("READY TO RECEIVE")
    receive(sock, filename)
    sock.close()
    print("--- %s seconds ---" % (time.time() - start_time))
