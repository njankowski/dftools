import argparse
import glob
import os
from PIL import Image
from formats import bm
from formats import pal


def from_bm(args):
    if args.external:
        args.external = os.path.abspath(args.external)
        if args.compatible:
            rgb_palette = pal.vga13h_to_rgb_compat(pal.read(args.external))
        else:
            rgb_palette = pal.vga13h_to_rgb(pal.read(args.external))
        print(f'Loaded external palette "{args.external}"')
    else:
        if args.compatible:
            rgb_palette = pal.load_internal_compat(args.palette)
        else:
            rgb_palette = pal.load_internal(args.palette)
        print(f'Loaded built-in palette "{args.palette}"')

    args.file = os.path.abspath(args.file)
    images = glob.glob(args.file)
    for image in images:
        imageName = os.path.splitext(image)[0]
        print(f'Converting "{image}"')
        converted_images = bm.to_images(bm.read(image), rgb_palette)
        for i in range(len(converted_images)):
            if len(converted_images) == 1:
                converted_images[i].save(f'{imageName}.png')
            else:
                converted_images[i].save(f'{imageName}({str(i)}).png')


def main():
    parser = argparse.ArgumentParser(prog='bmtool',
                                     description='Tool for Star Wars: Dark Forces BM graphics.')
    parser.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    parser.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')
    parser.add_argument('-c', '--compatible',
                        help='Map color output like DF2 (BMPDF). Recommended for debugging only.',
                        action='store_true')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    from_bm(args)


if __name__ == '__main__':
    main()
