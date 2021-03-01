import argparse, os
from formats.df import delt, pltt
from PIL import Image


def from_delt(args):
    args.file = os.path.abspath(args.file)
    args.palette = os.path.abspath(args.palette)

    rgb_palette = pltt.read(args.palette)
    delt_file = delt.read(args.file)
    delt.to_image(delt_file[2], delt_file[0], delt_file[1], rgb_palette).save(f'{os.path.splitext(args.file)[0]}.png')


def main():
    parser = argparse.ArgumentParser(prog='delttool',
                                     description='Tool for Star Wars: Dark Forces DELT graphics.')

    parser.add_argument('file', help='file to convert')
    parser.add_argument('palette', help='color palette for conversion')

    args = parser.parse_args()

    from_delt(args)


if __name__ == '__main__':
    main()
