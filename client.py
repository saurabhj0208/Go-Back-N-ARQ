import select
import sys
import pickle
import socket
import os
import time

server_name = sys.argv[1]
port_no = int(sys.argv[2])
filename = sys.argv[3]
N = int(sys.argv[4])
MSS = int(sys.argv[5])

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if not os.path.isfile(filename):
    exit(1)


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


def create_buffer():
    seq_no = 0
    buffer = list()
    with open(filename, "rb") as binary_file:
        data_block = binary_file.read()
        size = sys.getsizeof(data_block)
        for index in range(0, size, MSS):
            binary_file.seek(0, index)
            packet_data = binary_file.read(MSS)
            checksum = getChecksum(packet_data)
            if index <= size - MSS:
                buffer.append(pickle.dumps([seq_no, checksum, "0101010101010101", packet_data]))
            else:
                buffer.append(pickle.dumps([seq_no, checksum, "1111111111111111", packet_data]))
            seq_no += 1
    return buffer


# Main Function #

if __name__ == "__main__":
    start = time.time()
    ack_waiting = 0
    ack = 0
    timeout = 0.1
    data = create_buffer()
    while ack <= len(data) - 1:
        if (ack_waiting + ack) < len(data) and ack_waiting < N:
            for packet in data:
                if pickle.loads(packet)[0] == ack_waiting + ack:
                    ack_waiting += 1
                    clientSocket.sendto(packet, (server_name, port_no))
            continue
        else:
            receiving = select.select([clientSocket], [], [], timeout)
            if not receiving[0]:
                print("Timeout, sequence number = " + str(ack))
                ack_waiting = 0
                continue
            else:
                acknowledged_data, address = clientSocket.recvfrom(2048)
                acknowledged_data = pickle.loads(acknowledged_data)
                if acknowledged_data[2] != "1010101010101010":
                    continue

                if acknowledged_data[0] != ack:
                    ack_waiting = 0
                    continue
                else:
                    ack += 1
                    ack_waiting -= 1
    print("Transmission Time: " + str(time.time() - start) + " ms")
    clientSocket.close()
