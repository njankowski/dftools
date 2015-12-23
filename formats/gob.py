import struct


GOB_HEADER_SIZE = 8
GOB_INDEX_SIZE = 4
GOB_INDEX_ENTRY_SIZE = 21

GOB_INDEX_ENTRY_NAME_LENGTH = 13

GOB_MAX_SIZE = 2 ** 31 - 1

GOB_MIN_INDEX_OR_DATA_OFFSET = GOB_HEADER_SIZE


def is_valid_entry_name(name):
    if not (0 < len(name) < GOB_INDEX_ENTRY_NAME_LENGTH):
        return False
    try:
        name.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def get_gob_size(entries):
    meta_size = (GOB_HEADER_SIZE + GOB_INDEX_SIZE +
            GOB_INDEX_ENTRY_SIZE * len(entries))

    data_size = 0
    for entry in entries:
        data_size += len(entry[1])

    return (meta_size, data_size)


def read(filename):
    with open(filename, 'rb') as file:
        entries = []

        if file.read(4) != b'GOB\n':
            return

        index_offset = struct.unpack('<i', file.read(4))[0]

        file.seek(index_offset)
        num_entries = struct.unpack('<i', file.read(4))[0]

        for i in range(num_entries):
            offset = struct.unpack('<i', file.read(4))[0]
            length = struct.unpack('<i', file.read(4))[0]
            name = file.read(13).decode('ascii').rstrip('\0')
            data = b''

            if length > 0:
                next_entry = file.tell()

                file.seek(offset)
                data = file.read(length)
                file.seek(next_entry)

            entries.append((name, data))

        return entries


def write(filename, entries):
    meta_size, data_size = get_gob_size(entries)
    if (meta_size + data_size) > GOB_MAX_SIZE:
        raise Exception('entries cannot fit into GOB')

    for entry in entries:
        if not is_valid_entry_name(entry[0]):
            raise Exception('"' + entry[0] + '" is an invalid filename.')

    with open(filename, 'wb') as file:
        file.write(b'GOB\n')

        file.write(struct.pack('<i', GOB_MIN_INDEX_OR_DATA_OFFSET + data_size))

        for entry in entries:
            file.write(entry[1])

        file.write(struct.pack('<i', len(entries)))

        offset = GOB_MIN_INDEX_OR_DATA_OFFSET
        for entry in entries:
            file.write(struct.pack('<i', offset))
            file.write(struct.pack('<i', len(entry[1])))
            file.write(struct.pack('13s', entry[0].encode('ascii')))
            offset += len(entry[1])
