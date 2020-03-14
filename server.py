import sys
import pickle
import random
import socket
import os

port_number = int(sys.argv[1])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', port_number))

prob = float(sys.argv[3])

filename = sys.argv[2]
if os.path.isfile(filename):
    os.remove(filename)


def write(data_block):
    with open(filename, 'ab') as file:
        file.write(data_block)


def getChecksum(data_block):
    checksumValue = 0
    if len(data_block) % 2:
        data_block += "0"

    i = 0
    while i < len(data_block):
        val = ord(data_block[i]) + (ord(data_block[i + 1]) << 8)
        checksumValue += val
        i = i + 2

    checksumValue = checksumValue + (checksumValue >> 16)
    checksumValue = ~checksumValue & 0xffff
    return checksumValue


# Main Function

if __name__ == "__main__":
    packet_sequence = -1
    while True:
        data, address = server_socket.recvfrom(2048)
        data = pickle.loads(data)
        sequence_number = data[0]
        checksum = data[1]
        packet_type = data[2]
        packet_data = data[3]
        error = random.uniform(0, 1)

        if packet_type == "1111111111111111" or packet_type == "0101010101010101":
            if error > prob:
                if checksum == getChecksum(packet_data):
                    if sequence_number != packet_sequence + 1:
                        continue
                    else:
                        senddata = pickle.dumps([sequence_number, "0000000000000000", "1010101010101010"])
                        server_socket.sendto(senddata, address)
                        packet_sequence += 1
                        write(packet_data)
                        if packet_type == "1111111111111111":
                            break
            else:
                print("Packet loss, sequence number = " + str(sequence_number))
