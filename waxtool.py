import argparse, os
from formats.df import pal, wax
from PIL import Image


def from_wax(args):
    if args.external:
        args.external = os.path.abspath(args.external)
        rgb_palette = pal.vga13h_to_rgb(pal.read(args.external))
        print(f'Loaded external palette "{args.external}"')
    else:
        rgb_palette = pal.load_internal(args.palette)
        print(f'Loaded built-in palette "{args.palette}"')

    args.file = os.path.abspath(args.file)
    print(f'Converting "{args.file}"')
    if args.graymap:
        images = wax.to_images_graymap(wax.read(args.file))
    else:
        images = wax.to_images(wax.read(args.file), rgb_palette)
    waxName = os.path.splitext(args.file)[0]
    for image in images:
        image[1].save(f'{waxName}-{image[0]}.png')


def main():
    parser = argparse.ArgumentParser(prog='waxtool',
                                     description='Tool for Star Wars: Dark Forces WAX graphics.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-p', '--palette',
                        help='Built-in color palette to use during conversion. SECBASE when unspecified.',
                        choices=['ARC','BUYIT','DTENTION','EXECUTOR','FUELSTAT','GROMAS','IMPCITY','JABSHIP','NARSHADA','RAMSHED','ROBOTICS','SECBASE','SEWERS','TALAY','TESTBASE','WAIT'],
                        default='SECBASE')
    group.add_argument('-e', '--external',
                        help='Specifies an external color palette to load for conversion. Overrides --palette.)')
    group.add_argument('-g', '--graymap', action='store_true', help='Output grayscale image based on color palette index.')

    parser.add_argument('file', help='file to convert')

    args = parser.parse_args()

    from_wax(args)


if __name__ == "__main__":
    main()
