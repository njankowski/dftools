'''
Miscellaneous Test Code

Extracts all images in an Outlaws NWX image to the current directory.
'''
import struct
import sys
from PIL import Image

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        entries = []

        if f.read(4) != b'WAXF':
            print('Bad Magic Identifier')
            exit(-1)

        major_version = struct.unpack('<I', f.read(4))[0]
        if major_version != 0x00000002:
            print('Bad Major Version')
            exit(-1)

        minor_version = struct.unpack('<I', f.read(4))[0]
        if minor_version != 0x00000001:
            print('Bad Minor Version')
            exit(-1)

        scale_x = struct.unpack('<f', f.read(4))[0]
        scale_y = struct.unpack('<f', f.read(4))[0]

        cell_table_offset = struct.unpack('<I', f.read(4))[0]
        frame_table_offset = struct.unpack('<I', f.read(4))[0]
        choreography_table_offset = struct.unpack('<I', f.read(4))[0]


        f.seek(cell_table_offset)


        if f.read(4) != b'CELT':
            print('Bad Cell Table Identifier')
            exit(-1)

        cell_count = struct.unpack('<I', f.read(4))[0]
        cell_table_size = struct.unpack('<I', f.read(4))[0]

        cells = []

        for i in range(cell_count):
            cell_id = struct.unpack('<I', f.read(4))[0]
            cell_size = struct.unpack('<I', f.read(4))[0]
            cell_width = struct.unpack('<I', f.read(4))[0]
            cell_height = struct.unpack('<I', f.read(4))[0]
            cell_flags = struct.unpack('<I', f.read(4))[0]

            if cell_size == 1 and cell_width == 0:
                print("Empty Cell: " + str(i))
                # 0xCD Terminator
                f.read(1)
                continue

            # Bit 0 specifies what dimension to use for column table retrieval and decompression.
            # Just swap dimensions so we don't need to change any code...
            if cell_flags & 0x00000001 == 0x00000000:
                temp = cell_width
                cell_width = cell_height
                cell_height = temp

            cell_column_offset_table_position = f.tell()
            cell_column_offsets = []
            for j in range(cell_width):
                cell_column_offsets.append(struct.unpack('<I', f.read(4))[0])


            cell_decompressed_columns = []
            for column_offset in cell_column_offsets:
                f.seek(cell_column_offset_table_position + column_offset)

                pixel_count = 0
                pixels = []
                while pixel_count < cell_height:
                    control_byte = struct.unpack('B', f.read(1))[0]
                    if control_byte < 0x02:
                        pixels.append(f.read(1))
                        pixel_count += 1
                    elif control_byte % 2 == 0:
                        pixels.extend([f.read(((control_byte // 2) + 1))])
                        pixel_count += ((control_byte // 2) + 1)
                    else:
                        pixels.extend([f.read(1)] * ((control_byte // 2) + 1))
                        pixel_count += ((control_byte // 2) + 1)

                cell_decompressed_columns.append(b''.join(pixels))
            cells.append((cell_width, cell_height, (cell_flags & 0x00000001 == 0x00000000), b''.join(cell_decompressed_columns)))
            # 0xCD terminates the image? Why?
            f.read(1)
            #f.seek(cell_column_offset_table_position + cell_size)

        # Palette
        pcx_palette = Image.open('simms.pcx').palette.getdata()[1]
        pal = []
        for i in range(256):
            r = (i * 3) + 0
            g = (i * 3) + 1
            b = (i * 3) + 2
            pal.append((pcx_palette[r], pcx_palette[g], pcx_palette[b]))

        count = 0
        for cell in cells:
            width = cell[0]
            height = cell[1]
            dim_flip = cell[2]
            data = cell[3]

            image = Image.new("RGBA", (width, height))
            pixels = image.load()
            for row in range(height):
                for col in range(width):
                    if data[col * height + row] == 0:
                        alpha = 0
                    else:
                        alpha = 255
                    pixels[col, row] = (pal[data[col * height + row]][0],
                                        pal[data[col * height + row]][1],
                                        pal[data[col * height + row]][2],
                                        alpha)
            if not dim_flip:
                image.transpose(Image.FLIP_TOP_BOTTOM).save(str(count) + '.png')
            else:
                image.transpose(Image.ROTATE_270).save(str(count) + '.png')
            count += 1
