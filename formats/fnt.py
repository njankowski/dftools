import struct

class FntCharacter:
    def __init__(self):
        self.width = 0
        self.raw_data = b''

class Fnt:
    def __init__(self):
        self.height = 0
        self.unknown = 0
        self.data_size = 0
        self.first_character = 0
        self.last_character = 0

        self.fnt_characters = []

def read(filename):
    with open(filename, 'rb') as file:
        fnt = Fnt()

        if file.read(4) != b'FNT\x15':
            raise Exception('File does not have FNT magic identifier.')

        fnt.height = struct.unpack('B', file.read(1))[0]
        fnt.unknown = struct.unpack('B', file.read(1))[0]
        fnt.data_size = struct.unpack('<h', file.read(2))[0]
        fnt.first_character = struct.unpack('B', file.read(1))[0]
        fnt.last_character = struct.unpack('B', file.read(1))[0]
        # pad
        file.read(22)

        for i in range(fnt.last_character - fnt.first_character + 1):
            fnt_character = FntCharacter()
            fnt_character.width = struct.unpack('B', file.read(1))[0]
            fnt_character.raw_data = file.read(fnt_character.width * fnt.height)
            fnt.fnt_characters.append(fnt_character)

    return fnt

def to_image(fnt, rgba_palette):
    from PIL import Image
    from util import imaging

    height = fnt.height
    total_width = 0
    for character in fnt.fnt_characters:
        total_width += character.width + 10
    image = Image.new("RGBA", (total_width, height))

    x = 0
    for character in fnt.fnt_characters:
        image.paste(imaging.to_image(character.raw_data, fnt.height, character.width, rgba_palette).rotate(90), (x, 0))
        x += character.width + 10

    return image
