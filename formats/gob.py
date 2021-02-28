"""
Star Wars: Dark Forces
GOB Container Functions
"""
import string
import struct


GOB_HEADER_SIZE = 8
GOB_CATALOG_OFFSET_SIZE = 4
GOB_CATALOG_ENTRY_SIZE = 21

GOB_MAX_SIZE = 2 ** 31 - 1


class GOBException(Exception):
    pass


def is_valid_entry_name(filename):
    """Return whether a name is valid as an entry name.

    Checks a name against an assortment of DOS-like filename rules.

    :param filename: The name to check
    :return: bool
    """
    allowed = string.ascii_letters + string.digits + "_^$~!#%&-{}@`'()"
    reserved = ['CON', 'PRN', 'AUX', 'CLOCK$', 'NUL',
                'COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT0', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
                'LST', 'KEYBD$', 'SCREEN$', '$IDLE$', 'CONFIG$']

    # Cannot be empty or None.
    if not filename:
        return False

    # Separator cannot appear more than once.
    if filename.count('.') > 1:
        return False

    # Split into name and extension.
    s = filename.partition('.')
    name = s[0]
    separator = s[1]
    extension = s[2]

    # Check name length.
    name_len_ok = (0 < len(name) <= 8)
    # Check name characters.
    name_char_ok = all(c in allowed for c in name)
    # Check name reservation.
    name_reserved_ok = (name.upper() not in reserved)

    # Default to valid extension checks.
    ext_len_ok = True
    ext_char_ok = True

    # Check extension if a separator is present.
    # Must have a valid extension if separator is present.
    if separator:
        # Check extension length.
        ext_len_ok = (0 < len(extension) <= 3)
        # Check extension characters.
        ext_char_ok = all(c in allowed for c in name)
        # Reserved names do not apply to extensions.


    return ((name_len_ok and name_char_ok and  name_reserved_ok) and (ext_len_ok and ext_char_ok))


def get_gob_size(entries):
    """Return a tuple of size information given a list of entries.

    Projects the meta data size and raw data size of a GOB if it were created with the given list of entries.

    :param entries: List of GOB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    :return: A tuple containing meta data size and raw data size in number of bytes (meta_size, data_size)
    """
    # Header + Catalog Offset + Catalog
    meta_size = GOB_HEADER_SIZE + GOB_CATALOG_OFFSET_SIZE + (GOB_CATALOG_ENTRY_SIZE * len(entries))
    # Raw Data
    data_size = sum([len(entry[1]) for entry in entries])

    return (meta_size, data_size)


def read(filename):
    """Reads a GOB container and returns all stored files.

    :param filename: Path to the GOB to read
    :return: List of GOB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    """
    with open(filename, 'rb') as file:
        entries = []

        if file.read(4) != b'GOB\n':
            return

        catalog_offset = struct.unpack('<i', file.read(4))[0]

        file.seek(catalog_offset)
        num_entries = struct.unpack('<i', file.read(4))[0]

        for i in range(num_entries):
            data_offset = struct.unpack('<i', file.read(4))[0]
            data_length = struct.unpack('<i', file.read(4))[0]

            raw_name = file.read(13)
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


def write(filename, entries, strict_naming=True):
    """Writes a GOB container given a path and a list of GOB entries.

    :param filename: Path to write the GOB to
    :param entries: List of GOB entry tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the entry
    :param strict_naming: Check names against DOS filename rules
    :return: None
    """
    meta_size, data_size = get_gob_size(entries)
    if (meta_size + data_size) > GOB_MAX_SIZE:
        raise GOBException('Cannot create GOB because it would exceed maximum size.')

    if strict_naming:
        for entry in entries:
            if not is_valid_entry_name(entry[0]):
                raise GOBException('"' + entry[0] + '" is an invalid entry name.')

    with open(filename, 'wb') as file:
        file.write(b'GOB\n')

        file.write(struct.pack('<i', GOB_HEADER_SIZE + data_size))

        for entry in entries:
            file.write(entry[1])

        file.write(struct.pack('<i', len(entries)))

        offset = GOB_HEADER_SIZE
        for entry in entries:
            file.write(struct.pack('<i', offset))
            file.write(struct.pack('<i', len(entry[1])))
            file.write(struct.pack('13s', entry[0].encode('ascii')))
            offset += len(entry[1])
