import string
import struct


GOB_HEADER_SIZE = 8
GOB_INDEX_SIZE = 4
GOB_INDEX_ENTRY_SIZE = 21

GOB_MAX_SIZE = 2 ** 31 - 1

GOB_MIN_INDEX_OR_DATA_OFFSET = GOB_HEADER_SIZE


def is_valid_dos_name(filename):
    """Return whether a string is a valid DOS filename"""
    allowed = string.ascii_letters + string.digits + "_^$~!#%&-{}@`'()"
    reserved = ['CON', 'PRN', 'AUX', 'CLOCK$', 'NUL', 'COM0', 'COM1', 'COM2',
                'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT0',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8',
                'LPT9', 'LST', 'KEYBD$', 'SCREEN$', '$IDLE$', 'CONFIG$']

    # Filename cannot be empty or None.
    if not filename:
        return False

    # Period cannot appear more than once.
    if not filename.count('.') <= 1:
        return False


    s = filename.partition('.')
    name = s[0]

    # Name can be up to eight characters.
    name_len_ok = (0 < len(name) <= 8)
    # Name consists of only allowed characters.
    name_char_ok = all(c in allowed for c in name)
    # Name cannot be reserved.
    name_reserved_ok = (name.upper() not in reserved)

    if not (name_len_ok and name_char_ok and  name_reserved_ok):
        return False


    extension = s[2]

    # Extension can be excluded.
    if extension:
        # Extension can be up to three characters.
        ext_len_ok = (0 <= len(extension) <= 3)
        # Name consists of only allowed characters.
        ext_char_ok = all(c in allowed for c in name)

        if not (ext_len_ok and ext_char_ok):
            return False


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

            raw_name = file.read(13)
            name = raw_name[0 : raw_name.index(0)].decode('ascii')

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
        if not is_valid_dos_name(entry[0]):
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
