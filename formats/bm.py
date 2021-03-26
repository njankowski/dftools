import struct
from util import compression
from util import imaging

TRANSPARENCY_NONE = 0x36

class Bm:
    def __init__(self):
        self.x = 0
        self.y = 0
        self._idem_x = 0
        self._idem_y = 0
        self.transparent = 0
        self.log_size_y = 0
        self.compressed = 0
        self.data_size = 0
        self.raw_data = b''

        self.frame_rate = 0
        self.sub_bms = []

def read(filename):
    with open(filename, 'rb') as file:
        bm = Bm()
        identifier = file.read(4)
        # Identifier may erroneously omit the space character and split the \x1e byte across two bytes for some user generated files.
        if identifier != b'BM \x1e' and identifier != b'BM\x01\x0e':
            raise Exception("BM has no magic identifier.")

        bm.x = struct.unpack('<h', file.read(2))[0]
        bm.y = struct.unpack('<h', file.read(2))[0]
        bm._idem_x = struct.unpack('<h', file.read(2))[0]
        bm._idem_y = struct.unpack('<h', file.read(2))[0]
        bm.transparent = struct.unpack('B', file.read(1))[0]
        bm.log_size_y = struct.unpack('B', file.read(1))[0]
        bm.compressed = struct.unpack('<h', file.read(2))[0]
        bm.data_size = struct.unpack('<i', file.read(4))[0]
        # pad
        file.read(12)

        # multiple BMs
        if (bm.x == 1 and bm.y != 1):
            bm.frame_rate = struct.unpack('B', file.read(1))[0]
            if struct.unpack('B', file.read(1))[0] != 2:
                raise Exception("BM Multiple has bad magic identifier.")

            offset_table = []
            for i in range(bm._idem_y):
                offset_table.append(struct.unpack('<i', file.read(4))[0] + 34)

            for offset in offset_table:
                sub_bm = Bm()
                file.seek(offset)

                sub_bm.x = struct.unpack('<h', file.read(2))[0]
                sub_bm.y = struct.unpack('<h', file.read(2))[0]
                sub_bm._idem_x = struct.unpack('<h', file.read(2))[0]
                sub_bm._idem_y = struct.unpack('<h', file.read(2))[0]
                sub_bm.data_size = struct.unpack('<i', file.read(4))[0]
                sub_bm.log_size_y = struct.unpack('B', file.read(1))[0]
                # pad
                file.read(11)
                sub_bm.transparent = struct.unpack('B', file.read(1))[0]
                # pad
                file.read(3)

                sub_bm.raw_data = file.read(sub_bm.x * sub_bm.y)
                bm.sub_bms.append(sub_bm)
        else:
            if bm.compressed == 0:
                bm.raw_data = file.read()
            else:
                file.seek(bm.data_size + 32)
                offset_table = []
                for offset in range(bm.x):
                    offset_table.append(struct.unpack("<i", file.read(4))[0] + 32)

                if bm.compressed == compression.RLE0:
                    bm.raw_data = compression.rle0_decompress(file, bm.y, offset_table)
                else:
                    bm.raw_data = compression.rle1_decompress(file, bm.y, offset_table)


         # Try to catch certain BMs with bad header endianess.
        if not (bm.x == 1 and bm.y != 1) and (bm.compressed == 0) and (bm.data_size != 0) and ((bm.x * bm.y) != bm.data_size):
            #print('header may have incorrect endianess in multiple fields')
            #print('attempting swap')
            bm.x = ((bm.x & 0xFF00) >> 8) | ((bm.x & 0x00FF) << 8)
            bm.y = ((bm.y & 0xFF00) >> 8) | ((bm.y & 0x00FF) << 8)
            bm._idem_x = ((bm._idem_x & 0xFF00) >> 8) | ((bm._idem_x & 0x00FF) << 8)
            bm._idem_y = ((bm._idem_y & 0xFF00) >> 8) | ((bm._idem_y & 0x00FF) << 8)
            bm.compressed = ((bm.compressed & 0xFF00) >> 8) | ((bm.compressed & 0x00FF) << 8)
            bm.data_size = ((bm.data_size & 0xFF00) >> 8) | ((bm.data_size & 0x00FF) << 8)

        return bm

def write(filename, bm):
    with open(filename, 'wb') as file:
        compression_type = compression.calc_ideal_compression_bm(bm.raw_data, bm.y)
        if compression_type == compression.NONE:
            data_length = len(bm.raw_data)
            bm.compressed = compression.NONE
        elif compression_type == compression.RLE0:
            compressed_data = compression.rle0_compress(bm.raw_data, bm.y)
            data_length = len(compressed_data[0])
            bm.compressed = compression.RLE0
        elif compression_type == compression.RLE1:
            compressed_data = compression.rle1_compress(bm.raw_data, bm.y)
            data_length = len(compressed_data[0])
            bm.compressed = compression.RLE1

        file.write(b'BM \x1e')
        if bm.x == 1 and bm.y != 1:
            raise Exception()
        file.write(struct.pack('<h', bm.x))
        file.write(struct.pack('<h', bm.y))
        file.write(struct.pack('<h', bm._idem_x))
        file.write(struct.pack('<h', bm._idem_y))
        file.write(struct.pack('B', bm.transparent))
        file.write(struct.pack('B', bm.log_size_y))
        file.write(struct.pack('<h', bm.compressed))
        file.write(struct.pack('<i', data_length))
        file.write(b'\0' * 12)

        if bm.compressed == compression.NONE:
            file.write(bm.raw_data)
        else:
            file.write(bytes(compressed_data[0]))

        # Column table is at the end of the file.
        if bm.compressed != compression.NONE:
            for column_offset in compressed_data[1]:
                file.write(struct.pack("<i", column_offset))

def to_images(bm, rgb_palette):
    from PIL import Image
    images = []
    if not bm.sub_bms:
        if bm.transparent == TRANSPARENCY_NONE:
            images.append(imaging.to_image(bm.raw_data, bm.y, bm.x, rgb_palette, False).transpose(Image.ROTATE_90))
        else:
            images.append(imaging.to_image(bm.raw_data, bm.y, bm.x, rgb_palette, True).transpose(Image.ROTATE_90))
    else:
        for sub_bm in bm.sub_bms:
            if bm.transparent == TRANSPARENCY_NONE:
                images.append(imaging.to_image(sub_bm.raw_data, sub_bm.y,sub_bm.x, rgb_palette, False).transpose(Image.ROTATE_90))
            else:
                images.append(imaging.to_image(sub_bm.raw_data, sub_bm.y,sub_bm.x, rgb_palette, True).transpose(Image.ROTATE_90))
    return images
