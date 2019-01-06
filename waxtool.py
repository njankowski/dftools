import argparse
import os
from PIL import Image
from formats import pal
from formats import wax


def from_wax(args):
    if args.external:
        args.external = os.path.abspath(args.external)
        rgb_palette = pal.vga13h_to_rgb(pal.read(args.external))
        print(f'Loaded external palette "{args.external}"')
    else:
        rgb_palette = pal.default_palettes[args.palette]
        print(f'Loaded built-in palette "{args.palette}"')

    args.file = os.path.abspath(args.file)
    print(f'Converting "{args.file}"')
    images = wax.to_images(wax.read(args.file), rgb_palette)
    waxName = os.path.splitext(args.file)[0]
    for image in images:
        image[1].save(f'{waxName} {image[0]}.png')


def main():
    parser = argparse.ArgumentParser(prog='waxtool',
                                     description='Tool for Star Wars: Dark Forces WAX graphics.')

    parser.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    parser.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')

    parser.add_argument('file', help='file to convert')

    args = parser.parse_args()

    from_wax(args)


if __name__ == "__main__":
    main()
