import argparse
import glob
import os
from PIL import Image
from formats import cmp
from formats import pal


def from_cmp(args):
    if args.external:
        args.external = os.path.abspath(args.external)
        rgb_palette = pal.vga13h_to_rgb(pal.read(args.external))
        print(f'Loaded external palette "{args.external}"')
    else:
        rgb_palette = pal.load_internal(args.palette)
        print(f'Loaded built-in palette "{args.palette}"')


    args.file = os.path.abspath(args.file)
    images = glob.glob(args.file)
    for image in images:
        imageName = os.path.splitext(image)[0]
        print(f'Converting "{image}"')
        cmp.to_image(cmp.read(image), rgb_palette).save(f'{imageName}.png')


def main():
    parser = argparse.ArgumentParser(prog='cmptool',
                                     description='Tool for Star Wars: Dark Forces CMP graphics.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    group.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    from_cmp(args)


if __name__ == '__main__':
    main()
