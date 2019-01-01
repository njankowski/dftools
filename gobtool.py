import argparse
import os
from formats import gob
from util import bulkrw


def archive(args):
    # Normalize paths.
    args.directory = os.path.abspath(args.directory)
    args.gob = os.path.abspath(args.gob)

    print(f'Archiving "{args.directory}" into GOB "{args.gob}"')

    entries = bulkrw.read_files(args.directory, args.recursive)
    gob.write(args.gob, entries)

    print('Done')


def extract(args):
    # Normalize paths.
    args.directory = os.path.abspath(args.directory)
    args.gob = os.path.abspath(args.gob)

    print(f'Extracting "{args.gob}" into directory "{args.directory}"')

    entries = gob.read(args.gob)
    bad_entries = bulkrw.write_files(args.directory, entries, args.organize)

    if args.interactive and bad_entries:
        print('Some files could not be saved. Please provide a name for each file when prompted.')
        bulkrw.write_files_interactive(args.directory, bad_entries)
    elif bad_entries:
        print('Some files could not be saved. Use the "-i" or "--interactive" option to extract these files.')

    print('Done')


def inspect(args):
    pass


def main():
    parser = argparse.ArgumentParser(prog='gobtool', description='Tool for Star Wars: Dark Forces GOB archives.')
    subparsers = parser.add_subparsers(dest='cmd', required=True, help='the operation to perform')

    parser.add_argument('-v', '--verbose', action='store_true', help='print extra information')


    # Extract command subparser.
    extract_parser = subparsers.add_parser('extract', help='extract from a GOB')
    extract_parser.set_defaults(func=extract)
    extract_parser.add_argument('-o', '--organize', help='create a subdirectory for each file extension in the archive', action='store_true')
    extract_parser.add_argument('-i', '--interactive', help='manual renaming when extracting files with bad filenames', action='store_true')
    extract_parser.add_argument('gob', help='GOB to extract from')
    extract_parser.add_argument('directory', help='directory to extract into')


    # Archive command subparser.
    archive_parser = subparsers.add_parser('archive', help='archive into a GOB')
    archive_parser.set_defaults(func=archive)
    archive_parser.add_argument('-r', '--recursive', help='archive all files in the directory and its subdirectories', action='store_true')
    archive_parser.add_argument('directory', help='directory to archive from')
    archive_parser.add_argument('gob', help='GOB to archive into')


    # Inspect command subparser.
    inspect_parser = subparsers.add_parser('inspect', help='print information about a GOB')
    inspect_parser.set_defaults(func=inspect)
    inspect_parser.add_argument('gob', help='GOB to inspect')


    # Parse arguments.
    args = parser.parse_args()


    # Dispatch command.
    args.func(args)


if __name__ == '__main__':
    main()
