import struct


def read(filename):
    """Reads a GOB container and returns all stored files.

    :param filename: Path to the GOB to read
    :return: List of GOB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    """
    with open(filename, 'rb') as file:
        entries = []

        if file.read(4) != b'GOB ':
            return

        version = struct.unpack('<i', file.read(4))[0]
        if version != 0x14:
            return

        catalog_offset = struct.unpack('<i', file.read(4))[0]

        file.seek(catalog_offset)
        num_entries = struct.unpack('<i', file.read(4))[0]

        for i in range(num_entries):
            data_offset = struct.unpack('<i', file.read(4))[0]
            data_length = struct.unpack('<i', file.read(4))[0]

            raw_name = file.read(128)
            try:
                name = raw_name[0 : raw_name.index(0)].decode('ascii')
            except ValueError:
                name = raw_name.decode('ascii')
                print(f'catalog entry {i} has no null terminator in its filename "{name}"')

            data = b''

            if data_length > 0:
                next_entry = file.tell()

                file.seek(data_offset)
                data = file.read(data_length)
                file.seek(next_entry)

            entries.append((name, data))

        return entries
