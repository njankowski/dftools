import os, struct


def read(filename):
    with open(filename, 'rb') as file:
        entries = []

        name = os.path.splitext(os.path.basename(filename))[0]

        count = struct.unpack('<h', file.read(2))[0]

        for i in range(count):
            length = struct.unpack('<i', file.read(4))[0]
            entries.append((f'{name}_{i}.DELT', file.read(length)))

        return entries
