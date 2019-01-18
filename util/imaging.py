from PIL import Image
from formats import pal

def to_image(data, width, height, rgb_palette, transparency):
    image = Image.new("RGBA", (width, height))
    pixels = image.load()
    for row in range(height):
        for col in range(width):
            if transparency and data[row * width + col] == pal.TRANSPARENT_COLOR:
                alpha = 0
            else:
                alpha = 255
            pixels[col, row] = (rgb_palette[data[row * width + col]][0],
                                rgb_palette[data[row * width + col]][1],
                                rgb_palette[data[row * width + col]][2],
                                alpha)
    return image


def to_image_graymap(data, width, height):
    image = Image.new("RGBA", (width, height))
    pixels = image.load()
    for row in range(height):
        for col in range(width):
            pixels[col, row] = (data[row * width + col],
                                data[row * width + col],
                                data[row * width + col],
                                255)
    return image
