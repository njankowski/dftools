import argparse
import os
from PIL import Image
from formats import pal
from formats import wax


args = None


def extract_wax():
    if args.external:
        rgba_palette = pal.vga13h_to_rgba(pal.read(args.external))
        print('Loaded external palette "' + args.external + '"')
    else:
        rgba_palette = pal.default_palettes[args.palette]
        print('Loaded built-in palette "' + args.palette + '"')

    print('Converting "' + args.file + '"')
    images = wax.to_images(wax.read(args.file), rgba_palette)
    waxName = os.path.splitext(args.file)[0]
    for image in images:
        image[1].save(waxName + ' ' + image[0] + '.png')

    print('Done')


if __name__ == "__main__":
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

    extract_wax()
