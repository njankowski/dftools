import struct
from util import imaging


def read(filename):
    with open(filename, 'rb') as file:
        x_offset = struct.unpack('<h', file.read(2))[0]
        y_offset =  struct.unpack('<h', file.read(2))[0]
        x_size = struct.unpack('<h', file.read(2))[0] + 1
        y_size = struct.unpack('<h', file.read(2))[0] + 1

        true_x_size = x_offset + x_size
        true_y_size = y_offset + y_size

        pixels = [0] * (true_x_size * true_y_size)

        while True:
            size_and_type = struct.unpack('<H', file.read(2))[0]

            if size_and_type == 0:
                break

            start_x = struct.unpack('<h', file.read(2))[0]
            start_y = struct.unpack('<h', file.read(2))[0]

            just_size = size_and_type >> 1
            just_type = size_and_type & 0b1

            # Uncompressed
            if just_type == 0:
                data = list(file.read(just_size))
                index = (start_y * true_x_size) + start_x
                pixels[index:index+len(data)] = data
            # Compressed
            elif just_type == 1:
                data = []
                i = 0
                while i < just_size:
                    control_byte = struct.unpack('B', file.read(1))[0]
                    count = control_byte >> 1
                    compressed = control_byte & 0b1
                    if compressed == 0:
                        data += file.read(count)
                    elif compressed == 1:
                        color = [struct.unpack('B', file.read(1))[0]]
                        data += color * count
                    else:
                        return
                    i += count
                if i != just_size:
                    return
                index = (start_y * true_x_size) + start_x
                pixels[index:index+len(data)] = data
            else:
                return

        return (true_x_size, true_y_size, pixels)


def to_image(data, width, height, rgb_palette):
    from PIL import Image
    image = imaging.to_image(data, width, height, rgb_palette, True)
    return image
