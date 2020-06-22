import sys
import socket
# Main function
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SENDER_ADDR)
    filename = "../data/small-data.txt"

    start_time = time.time()
    send(sock, filename)
    sock.close()
    print("--- %s seconds ---" % (time.time() - start_time))

