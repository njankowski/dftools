import struct


def read(filename):
    with open(filename, 'rb') as file:
        entries = []

        count = struct.unpack('<h', file.read(2))[0]

        for i in range(count):
            length = struct.unpack('<i', file.read(4))[0]
            entries.append(file.read(length))

        return entries
