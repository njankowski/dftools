"""
Star Wars: Dark Forces colormap functions.

A Dark Forces colormap maps colors to other colors in the palette
depending on the surrounding light value. It also contains a
gradient for the headlamp.
"""
from formats import pal

# Some notes on the colormap.

# When mapping a color with a light level, 0 is COMPLETE DARKNESS
# and 31 is COMPLETE BRIGHTNESS.

# The last 128 bytes of the colormap are a gradient map for
# the headlamp depending on distance. The first byte is closest
# to the player.

# Size of colormap in bytes.
# 8320 bytes.
CMP_SIZE = (256 * 31) + 255 + 128 + 1

# Maximum light level.
MAX_LIGHT = 31
MAX_HEADLAMP_DISTANCE = 127


def read(filename):
    with open(filename, "rb") as file:
        return list(file.read(CMP_SIZE))


def write(filename, colormap):
    if not is_valid_colormap(colormap):
        raise Exception("size does not match a colormap")

    with open(filename, "wb") as file:
        file.write(bytes(colormap))


def is_valid_colormap(colormap):
    if len(colormap) != CMP_SIZE:
        return False

    return True


def map_color(colormap, light, color):
    if not (0 <= light <= MAX_LIGHT):
        raise ValueError("light value is out of range")
    if not (0 <= color < pal.NUM_COLORS):
        raise ValueError("color value is out of range")

    return colormap[(256 * light) + color]


def map_headlamp_gradient(colormap, distance):
    if not (0 <= distance <= MAX_HEADLAMP_DISTANCE):
        raise ValueError("distance value is out of range")

    return colormap[(len(colormap) - 128) + distance]
