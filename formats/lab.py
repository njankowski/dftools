import struct


LAB_HEADER_SIZE = 16
LAB_CATALOG_ENTRY_SIZE = 16
LAB_MAX_SIZE = 2 ** 31 - 1


def get_lab_size(entries):
    pass


def read_until_null(file):
    s = bytearray()
    c = file.read(1)
    while c != b'\x00':
        s.extend(c)
        c = file.read(1)
    return bytes(s)


def read(filename):
    with open(filename, 'rb') as file:
        entries = []

        if file.read(4) != b'LABN':
            return

        version = struct.unpack('<i', file.read(4))[0]

        if version != 0x00010000:
            return

        num_entries = struct.unpack('<i', file.read(4))[0]
        name_table_len = struct.unpack('<i', file.read(4))[0]

        name_table_start = LAB_HEADER_SIZE + (num_entries * LAB_CATALOG_ENTRY_SIZE)

        for i in range(num_entries):
            name_offset = struct.unpack('<i', file.read(4))[0]
            data_offset = struct.unpack('<i', file.read(4))[0]
            data_length = struct.unpack('<i', file.read(4))[0]
            fourcc = file.read(4).decode('ascii')

            data = b''

            if data_offset > 0:
                next_entry = file.tell()

                file.seek(name_table_start + name_offset)
                name = read_until_null(file).decode('ascii')

                file.seek(data_offset)
                data = file.read(data_length)

                file.seek(next_entry)

            entries.append((name, data))

        return entries


def write(filename, entries):
    pass
