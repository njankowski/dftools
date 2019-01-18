import argparse
import glob
import os
from PIL import Image
from formats import pal


def from_pal(args):
    args.file = os.path.abspath(args.file)
    images = glob.glob(args.file)
    for image in images:
        imageName = os.path.splitext(image)[0]
        print(f'Converting "{image}"')
        pal.to_image(pal.vga13h_to_rgb(pal.read(image))).save(f'{imageName}.png')


def main():
    parser = argparse.ArgumentParser(prog='paltool',
                                     description='Tool for Star Wars: Dark Forces PAL graphics.')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    from_pal(args)


if __name__ == '__main__':
    main()
