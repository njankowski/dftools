import argparse
import glob
import os
from PIL import Image
from formats import fme
from formats import pal
from util import bulkrw


args = None


def convert_fme():
    if args.palette in pal.default_palettes:
        rgba_palette = pal.default_palettes[args.palette]
        print('Loaded built-in palette "' + args.palette + '"')
    else:
        rgba_palette = pal.vga13h_to_rgba(pal.read(args.palette))
        print('Loaded external palette "' + args.palette + '"')

    images = glob.glob(args.file)
    for image in images:
        imageName = os.path.splitext(image)[0]
        print('Converting "' + image + '"')
        fme.to_image(fme.read(image), rgba_palette).save(imageName + ".png")

    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='fme',
                                     description='Tool for Star Wars: Dark Forces FME graphics.')
    parser.add_argument('-p', '--palette',
                        help='PAL (color palette) to use during conversion. Specify a built-in palette or a PAL file to load. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    convert_fme()
