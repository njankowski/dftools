"""
Outlaws
LAB Container Functions
"""
import struct


LAB_HEADER_SIZE = 16
LAB_CATALOG_ENTRY_SIZE = 16

LAB_MAX_SIZE = 2 ** 31 - 1


class LABException(Exception):
    pass


def is_valid_entry_name(filename):
    """Return whether a name is valid as an entry name.

    :param filename: The name to check
    :return: bool
    """
    # Fix Me
    return True


def get_lab_size(entries):
    """Return a tuple of size information given a list of entries.

    Projects the meta data size and raw data size of a LAB if it were created with the given list of entries.

    :param entries: List of LAB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    :return: A tuple containing meta data size and raw data size in number of bytes (meta_size, data_size)
    """
    # Header + Catalog + Name Table
    meta_size = LAB_HEADER_SIZE + (LAB_CATALOG_ENTRY_SIZE * len(entries)) + (sum([(len(entry[0]) + 1) for entry in entries]))
    # Raw Data
    data_size = sum([len(entry[1]) for entry in entries])

    return (meta_size, data_size)


def read(filename):
    """Reads a LAB container and returns all stored files.

    :param filename: Path to the LAB to read
    :return: List of LAB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    """
    # Utility function for reading null-terminated names.
    def read_until_null(file):
        s = bytearray()
        c = file.read(1)
        while c != b'\x00':
            s.extend(c)
            c = file.read(1)
        return bytes(s)


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

            next_entry = file.tell()
            file.seek(name_table_start + name_offset)
            name = read_until_null(file).decode('ascii')

            data = b''

            if data_length > 0:
                file.seek(data_offset)
                data = file.read(data_length)

            file.seek(next_entry)

            entries.append((name, data))

        if sum([(len(entry[0]) + 1) for entry in entries]) != name_table_len:
            return

        return entries


def write(filename, entries):
    """Writes a LAB container given a path and a list of LAB entries.

    :param filename: Path to write the LAB to
    :param entries: List of LAB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    :return: None
    """
    meta_size, data_size = get_lab_size(entries)
    if (meta_size + data_size) > LAB_MAX_SIZE:
        raise LABException('Cannot create LAB because it would exceed maximum size.')

    for entry in entries:
        if not is_valid_entry_name(entry[0]):
            raise LABException('"' + entry[0] + '" is an invalid entry name.')

    with open(filename, 'wb') as file:
        file.write(b'LABN')
        file.write(struct.pack('<i', 0x00010000))
        file.write(struct.pack('<i', len(entries)))
        name_table_len = sum([(len(entry[0]) + 1) for entry in entries])
        file.write(struct.pack('<i', name_table_len))

        name_offset = 0
        data_offset = LAB_HEADER_SIZE + (LAB_CATALOG_ENTRY_SIZE * len(entries)) + name_table_len
        for entry in entries:
            file.write(struct.pack('<i', name_offset))
            file.write(struct.pack('<i', data_offset))
            file.write(struct.pack('<i', len(entry[1])))
            # Fix Me
            file.write(struct.pack('<i', 0)))

            name_offset += len(entry[0]) + 1
            data_offset += len(entry[1])

        for entry in entries:
            file.write(entry[1])
