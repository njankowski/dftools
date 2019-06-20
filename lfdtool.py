import argparse
import os
from formats import lfd
from util import bulkrw


def archive(args):
    pass


def extract(args):
    # Normalize paths.
    args.directory = os.path.abspath(args.directory)
    args.lfd = os.path.abspath(args.lfd)

    print(f'Extracting "{args.lfd}" into directory "{args.directory}"')

    entries = lfd.read(args.lfd)
    bad_entries = bulkrw.write_files(args.directory, entries, args.organize)

    if args.interactive and bad_entries:
        print('Some files could not be saved. Please provide a name for each file when prompted.')
        bulkrw.write_files_interactive(args.directory, bad_entries)
    elif bad_entries:
        print('Some files could not be saved. Use the "-i" or "--interactive" option to extract these files.')


def main():
    parser = argparse.ArgumentParser(prog='lfdtool', description='Tool for Star Wars: Dark Forces LFD archives.')
    subparsers = parser.add_subparsers(dest='cmd', required=True, help='the operation to perform')

    parser.add_argument('-v', '--verbose', action='store_true', help='print extra information')


    # Extract command subparser.
    extract_parser = subparsers.add_parser('extract', help='extract from an LFD')
    extract_parser.set_defaults(func=extract)
    extract_parser.add_argument('-o', '--organize', help='create a subdirectory for each file extension in the archive', action='store_true')
    extract_parser.add_argument('-i', '--interactive', help='manual renaming when extracting files with bad filenames', action='store_true')
    extract_parser.add_argument('lfd', help='LFD to extract from')
    extract_parser.add_argument('directory', help='directory to extract into')


    # Parse arguments.
    args = parser.parse_args()


    # Dispatch command.
    args.func(args)


if __name__ == '__main__':
    main()
