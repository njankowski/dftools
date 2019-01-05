import argparse
import glob
import os
from PIL import Image
from formats import bm
from formats import pal


args = None


def convert_bm():
    if args.external:
        rgb_palette = pal.vga13h_to_rgb(pal.read(args.external))
        print('Loaded external palette "' + args.external + '"')
    else:
        rgb_palette = pal.default_palettes[args.palette]
        print('Loaded built-in palette "' + args.palette + '"')

    images = glob.glob(args.file)
    for image in images:
        imageName = os.path.splitext(image)[0]
        print('Converting "' + image + '"')
        converted_images = bm.to_images(bm.read(image), rgb_palette)
        for i in range(len(converted_images)):
            if len(converted_images) == 1:
                converted_images[i].save(imageName + '.png')
            else:
                converted_images[i].save(imageName + ' ('+ str(i) + ')' + '.png')
    print('Done')


def main():
    parser = argparse.ArgumentParser(prog='bmtool',
                                     description='Tool for Star Wars: Dark Forces BM graphics.')
    parser.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    parser.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    convert_bm()


if __name__ == '__main__':
    main()
