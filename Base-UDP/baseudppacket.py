# Creates an empty packet
def make_empty():
    return b''


def make_datagram(data=b''):
    return data


def extract_datagram(packet):
    return packet[4:]
