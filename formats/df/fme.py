import struct
from util import compression
from util import imaging


DISPLAY_PROP_SIZE = 32
DATA_PROP_SIZE = 24


class FmeDisplayProperties:
    def __init__(self):
        self.x_offset = 0
        self.y_offset = 0
        self.flip = 0
        self._data_properties_offset = 0
        self._unit_width = 0
        self._unit_height = 0
        self._pad0 = 0
        self._pad1 = 0


class FmeDataProperties:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.compressed = 0
        self._data_size = 0
        self._column_offset = 0
        self._pad0 = 0
        self.raw = b""


class Fme:
    def __init__(self):
        self.display = FmeDisplayProperties()
        self.data = FmeDataProperties()


def read(filename):
    display = FmeDisplayProperties()
    data = FmeDataProperties()

    with open(filename, "rb") as file:
        display.x_offset = struct.unpack("<i", file.read(4))[0]
        display.y_offset = struct.unpack("<i", file.read(4))[0]
        display.flip = struct.unpack("<i", file.read(4))[0]
        display._data_properties_offset = struct.unpack("<i", file.read(4))[0]
        display._unit_width = struct.unpack("<i", file.read(4))[0]
        display._unit_height = struct.unpack("<i", file.read(4))[0]
        display._pad0 = struct.unpack("<i", file.read(4))[0]
        display._pad1 = struct.unpack("<i", file.read(4))[0]

        file.seek(display._data_properties_offset)

        data.x = struct.unpack("<i", file.read(4))[0]
        data.y = struct.unpack("<i", file.read(4))[0]
        data.compressed = struct.unpack("<i", file.read(4))[0]
        data._data_size = struct.unpack("<i", file.read(4))[0]
        data._column_offset = struct.unpack("<i", file.read(4))[0]
        data._pad0 = struct.unpack("<i", file.read(4))[0]

        if (data.compressed == 0):
            data.raw = file.read()
        else:
            file.seek(data._column_offset + DISPLAY_PROP_SIZE + DATA_PROP_SIZE)

            offset_table = []
            for offset in range(data.x):
                offset_table.append(struct.unpack("<i", file.read(4))[0] + display._data_properties_offset)

            data.raw = compression.rle0_decompress(file, data.y, offset_table)

        fme = Fme()
        fme.display = display
        fme.data = data

    return fme

def read_from_wax(file):
    display = FmeDisplayProperties()
    data = FmeDataProperties()

    display.x_offset = struct.unpack("<i", file.read(4))[0]
    display.y_offset = struct.unpack("<i", file.read(4))[0]
    display.flip = struct.unpack("<i", file.read(4))[0]
    display._data_properties_offset = struct.unpack("<i", file.read(4))[0]
    display._unit_width = struct.unpack("<i", file.read(4))[0]
    display._unit_height = struct.unpack("<i", file.read(4))[0]
    display._pad0 = struct.unpack("<i", file.read(4))[0]
    display._pad1 = struct.unpack("<i", file.read(4))[0]

    file.seek(display._data_properties_offset)

    data.x = struct.unpack("<i", file.read(4))[0]
    data.y = struct.unpack("<i", file.read(4))[0]
    data.compressed = struct.unpack("<i", file.read(4))[0]
    data._data_size = struct.unpack("<i", file.read(4))[0]
    data._column_offset = struct.unpack("<i", file.read(4))[0]
    data._pad0 = struct.unpack("<i", file.read(4))[0]

    if (data.compressed == 0):
        data.raw = file.read()
    else:
        offset_table = []
        for offset in range(data.x):
            # Offset points right to the column. No special offset.
             offset_table.append(struct.unpack("<i", file.read(4))[0] + display._data_properties_offset)

        data.raw = compression.rle0_decompress(file, data.y, offset_table)

    fme = Fme()
    fme.display = display
    fme.data = data

    return fme


def write(filename, fme):
    with open(filename, "wb") as file:
        compression_type = compression.calc_ideal_compression_fme(fme.data.raw, fme.data.y)
        # RLE1 not allowed.
        if compression_type == compression.NONE:
            data_length = len(fme.data.raw)
            fme.data.compressed = 0
        else:
            compressed_data = compression.rle0_compress(fme.data.raw, fme.data.y)
            data_length = len(compressed_data[0])
            fme.data.compressed = 1

        file.write(struct.pack("<i", fme.display.x_offset))
        file.write(struct.pack("<i", fme.display.y_offset))
        file.write(struct.pack("<i", fme.display.flip))
        file.write(struct.pack("<i", DISPLAY_PROP_SIZE))
        file.write(struct.pack("<i", fme.display._unit_width))
        file.write(struct.pack("<i", fme.display._unit_height))
        file.write(struct.pack("<i", 0))
        file.write(struct.pack("<i", 0))

        file.write(struct.pack("<i", fme.data.x))
        file.write(struct.pack("<i", fme.data.y))
        file.write(struct.pack("<i", fme.data.compressed))

        if fme.data.compressed == 0:
            file.write(struct.pack("<i", DATA_PROP_SIZE + data_length))
        else:
            file.write(struct.pack("<i", DATA_PROP_SIZE + data_length + fme.data.x * 4))
        file.write(struct.pack("<i", 0))
        file.write(struct.pack("<i", 0))

        # Only write column table when compressed.
        if fme.data.compressed == 1:
            for column_offset in compressed_data[1]:
                file.write(struct.pack("<i", fme.data.x * 4 + DATA_PROP_SIZE + column_offset))

        if fme.data.compressed == 0:
            file.write(fme.data.raw)
        else:
            file.write(bytes(compressed_data[0]))


def to_image_graymap(fme):
    from PIL import Image
    image = imaging.to_image_graymap(fme.data.raw, fme.data.y, fme.data.x).transpose(Image.ROTATE_90)
    if fme.display.flip == 1:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image


def to_image(fme, rgb_palette):
    from PIL import Image
    image = imaging.to_image(fme.data.raw, fme.data.y, fme.data.x, rgb_palette, True).transpose(Image.ROTATE_90)
    if fme.display.flip == 1:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image
