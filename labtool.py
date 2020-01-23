import argparse
import os
from formats import lab
from util import bulkrw


def archive(args):
    args.directory = os.path.abspath(args.directory)
    args.lab = os.path.abspath(args.lab)

    print(f'Archiving "{args.directory}" into LAB "{args.lab}"')

    entries = bulkrw.read_files(args.directory, args.recursive)
    lab.write(args.lab, entries)

    print('Done')


def extract(args):
    args.directory = os.path.abspath(args.directory)
    args.lab = os.path.abspath(args.lab)

    print(f'Extracting "{args.lab}" into directory "{args.directory}"')

    entries = lab.read(args.lab)
    bad_entries = bulkrw.write_files(args.directory, entries, args.organize)

    if args.interactive and bad_entries:
        print('Some files could not be saved. Please provide a name for each file when prompted.')
        bulkrw.write_files_interactive(args.directory, bad_entries)
    elif bad_entries:
        print('Some files could not be saved. Use the "-i" or "--interactive" option to extract these files.')

    print('Done')


def main():
    parser = argparse.ArgumentParser(prog='labtool', description='Tool for Outlaws LAB archives.')
    subparsers = parser.add_subparsers(dest='cmd', required=True, help='the operation to perform')

    # Extract command subparser.
    extract_parser = subparsers.add_parser('extract', help='extract from a LAB')
    extract_parser.set_defaults(func=extract)
    extract_parser.add_argument('-o', '--organize', help='create a subdirectory for each file extension in the archive', action='store_true')
    extract_parser.add_argument('-i', '--interactive', help='manual renaming when extracting files with bad filenames', action='store_true')
    extract_parser.add_argument('lab', help='LAB to extract from')
    extract_parser.add_argument('directory', help='directory to extract into')


    # Archive command subparser.
    archive_parser = subparsers.add_parser('archive', help='archive into a LAB')
    archive_parser.set_defaults(func=archive)
    archive_parser.add_argument('-r', '--recursive', help='archive all files in the directory and its subdirectories', action='store_true')
    archive_parser.add_argument('directory', help='directory to archive from')
    archive_parser.add_argument('lab', help='LAB to archive into')


    # Parse arguments.
    args = parser.parse_args()

    # Dispatch command.
    args.func(args)


if __name__ == '__main__':
    main()
