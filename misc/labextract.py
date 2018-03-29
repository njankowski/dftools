'''
Miscellaneous Test Code

Extracts all entries in an Outlaws LAB archive to the current directory.
'''
import struct
import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        entries = []

        if f.read(4) != b'LABN':
            print('Bad Magic Identifier')
            exit(-1)

        version = struct.unpack('<I', f.read(4))[0]
        if version != 0x00010000:
            print('Bad Version')
            print('Continuing...')

        num_entries = struct.unpack('<I', f.read(4))[0]

        name_table_length = struct.unpack('<I', f.read(4))[0]

        catalog = []
        for i in range(num_entries):
            offset_name = struct.unpack('<I', f.read(4))[0]
            offset_data = struct.unpack('<I', f.read(4))[0]
            length_data = struct.unpack('<I', f.read(4))[0]
            four_cc = struct.unpack('<I', f.read(4))[0]
            catalog.append((offset_name, offset_data, length_data, four_cc))

        name_table_offset = f.tell()

        names = []
        for i in range(num_entries):
            f.seek(catalog[i][0], 1)

            raw_name = b''
            name = ''
            if i < num_entries - 1:
                raw_name = f.read(catalog[i + 1][0] - catalog[i][0])
                name = raw_name[0 : raw_name.index(0)].decode('ascii')
            else:
                raw_name = f.read((name_table_length + name_table_offset) - catalog[i][0])
                name = raw_name[0 : raw_name.index(0)].decode('ascii')

            f.seek(name_table_offset)

            names.append(name)

        f.seek((name_table_length + name_table_offset))

        for i in range(num_entries):
            entry = catalog[i]
            name = names[i]
            f.seek(entry[1])
            with open(name, 'wb') as e:
                e.write(f.read(entry[2]))
