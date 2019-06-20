import struct


def read(filename):
    with open(filename, 'rb') as file:
        entries = []

        if file.read(4) != b'RMAP':
            return

        name = file.read(8)
        if name != b'resource':
            return

        catalog_size = struct.unpack('<i', file.read(4))[0]
        if catalog_size % 16 != 0:
            return

        num_entries = catalog_size // 16

        catalog = []
        for i in range(num_entries):
            resource_type = file.read(4).decode('ascii')
            raw_name = file.read(8)
            if 0 in raw_name:
                name = raw_name[0 : raw_name.index(0)].decode('ascii')
            else:
                name = raw_name.decode('ascii')
            length = struct.unpack('<i', file.read(4))[0]
            catalog.append((resource_type, name, length))

        entries = []
        for i in range(num_entries):
            expected_resource_type = catalog[i][0]
            expected_name = catalog[i][1]
            expected_length = catalog[i][2]

            resource_type = file.read(4).decode('ascii')
            raw_name = file.read(8)
            if 0 in raw_name:
                name = raw_name[0 : raw_name.index(0)].decode('ascii')
            else:
                name = raw_name.decode('ascii')
            length = struct.unpack('<i', file.read(4))[0]

            if resource_type != expected_resource_type:
                return
            elif expected_name != name:
                return
            elif expected_length != length:
                return

            data = file.read(length)

            entries.append((f'{name}.{resource_type}', data))

        return entries
