import argparse
import glob
import os
from PIL import Image
from formats import fnt
from formats import pal


args = None


def convert_fnt():
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
        fnt.to_image(fnt.read(image), rgb_palette).save(imageName + '.png')

    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='fnt',
                                     description='Tool for Star Wars: Dark Forces FNT graphics.')
    parser.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    parser.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    convert_fnt()
