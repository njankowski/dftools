import struct


def read(filename):
    with open(filename, 'rb') as file:
        entries = []

        # RMAP should be the first entry.
        if file.read(4) != b'RMAP':
            return

        # RMAP has a specific name.
        raw_name = file.read(8)
        if 0 in raw_name:
            name = raw_name[0:raw_name.index(0)].decode('ascii')
        else:
            name = raw_name
        if name != b'resource':
            return

        # Get the total length of the following resource headers.
        index_size = struct.unpack('<i', file.read(4))[0]
        if index_size % 16 != 0:
            return

        num_entries = index_size // 16
