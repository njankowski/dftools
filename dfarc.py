import argparse
import os
import sys
from formats import gob, lab, lfd
from util import bulkrw


read_functions = {
    'gob': gob.read,
    'lab': lab.read,
    'lfd': lfd.read
}


write_functions = {
    'gob': gob.write,
    'lab': None,
    'lfd': None
}


def do_extract(args):
    args.directory = os.path.abspath(args.directory)
    args.container = os.path.abspath(args.container)

    if not os.path.isfile(args.container):
        sys.exit(f'"{args.container}" is not a container file to extract from.')\

    if not args.overwrite and os.path.isdir(args.directory):
        sys.exit(f'Cannot extract to "{args.directory}" because it already exists.\nUse the "-f" or "--overwrite" option to overwrite the directory.')

    extension = os.path.splitext(os.path.basename(args.container))[1].lower().lstrip('.')

    if extension not in read_functions:
        sys.exit(f'Unknown container type "{extension}"')

    print(f'Extracting "{args.container}" into "{args.directory}"')

    read_function = read_functions[extension]
    if read_function:
        entries = read_function(args.container)
    else:
        sys.exit(f'Extraction for {extension.upper()} containers is not available.')

    bad_entries = bulkrw.write_files(args.directory, entries, args.organize, args.overwrite)

    if args.interactive and bad_entries:
        print('Some files could not be saved. Please provide a name for each file when prompted.')
        bulkrw.write_files_interactive(args.directory, bad_entries)
    elif bad_entries:
        print('Some files could not be saved. Use the "-i" or "--interactive" option to extract these files.')

    print('Done')


def do_create(args):
    args.directory = os.path.abspath(args.directory)
    args.container = os.path.abspath(args.container)

    if not os.path.isdir(args.directory):
        sys.exit(f'"{args.container}" is not a directory to create from.')\

    if not args.overwrite and os.path.isfile(args.container):
        sys.exit(f'Cannot create "{args.directory}" because it already exists.\nUse the "-f" or "--overwrite" option to overwrite the container.')

    extension = os.path.splitext(os.path.basename(args.container))[1].lower().lstrip('.')

    if extension not in write_functions:
        sys.exit(f'Unknown container type "{extension}"')

    print(f'Creating "{args.container}" from "{args.directory}"')

    entries = bulkrw.read_files(args.directory, args.recursive)

    write_function = write_functions[extension]
    if write_function:
        write_function(args.container, entries)
    else:
        sys.exit(f'Creation for {extension.upper()} containers is not available.')

    print('Done')


def main():
    parser = argparse.ArgumentParser(prog='dfarc', description='Tool for Star Wars: Dark Forces and Outlaws containers.')
    parser.add_argument('-v', '--verbose', help='print extra information', action='store_true')
    subparsers = parser.add_subparsers(dest='cmd', required=True)

    extract_parser = subparsers.add_parser('extract', help='extract from a container')
    extract_parser.set_defaults(func=do_extract)
    extract_parser.add_argument('-f', '--overwrite', help='overwrite existing directories when extracting', action='store_true')
    extract_parser.add_argument('-i', '--interactive', help='manual renaming when extracting files with bad filenames', action='store_true')
    extract_parser.add_argument('-o', '--organize', help='create a subdirectory for each file extension in the container', action='store_true')
    extract_parser.add_argument('container', help='container to extract from')
    extract_parser.add_argument('directory', help='directory to extract into')

    create_parser = subparsers.add_parser('create', help='create a container')
    create_parser.set_defaults(func=do_create)
    create_parser.add_argument('-f', '--overwrite', help='overwrite existing container files when creating', action='store_true')
    create_parser.add_argument('-r', '--recursive', help='pack all files in the directory and its subdirectories', action='store_true')
    create_parser.add_argument('directory', help='directory to pack from')
    create_parser.add_argument('container', help='container to create')

    if len(sys.argv) == 1:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == 'archive':
        sys.argv[1] = 'create'

    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
