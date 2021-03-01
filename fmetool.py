import argparse, glob, os
from formats.df import fme, pal
from PIL import Image


def from_fme(args):
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
        if args.graymap:
            fme.to_image_graymap(fme.read(image)).save(f'{imageName}.png')
        else:
            fme.to_image(fme.read(image), rgb_palette).save(f'{imageName}.png')


def main():
    parser = argparse.ArgumentParser(prog='fmetool',
                                     description='Tool for Star Wars: Dark Forces FME graphics.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    group.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')
    group.add_argument('-g', '--graymap', action='store_true', help='Output grayscale image based on color palette index.')

    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    from_fme(args)


if __name__ == '__main__':
    main()
