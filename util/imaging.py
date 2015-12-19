from PIL import Image

def to_image(data, width, height, rgba_palette):
    image = Image.new("RGBA", (width, height))
    pixels = image.load()
    for row in range(height):
        for col in range(width):
            pixels[col, row] = (rgba_palette[data[row * width + col]][0],
                                rgba_palette[data[row * width + col]][1],
                                rgba_palette[data[row * width + col]][2],
                                rgba_palette[data[row * width + col]][3])
    return image
