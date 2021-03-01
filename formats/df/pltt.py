import struct


def read(filename):
    palette = []

    with open(filename, "rb") as file:
        first_color = struct.unpack("B", file.read(1))[0]
        last_color = struct.unpack("B", file.read(1))[0]

        num_colors = (last_color - first_color) + 1

        for color in range(num_colors):
            r = struct.unpack("B", file.read(1))[0]
            g = struct.unpack("B", file.read(1))[0]
            b = struct.unpack("B", file.read(1))[0]
            palette.append((r, g, b))

        pad = struct.unpack("B", file.read(1))[0]

        return palette
