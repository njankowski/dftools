import argparse
import os
from formats import anim
from util import bulkrw


def archive(args):
    pass


def extract(args):
    # Normalize paths.
    args.directory = os.path.abspath(args.directory)
    args.anim = os.path.abspath(args.anim)

    print(f'Extracting "{args.anim}" into directory "{args.directory}"')

    entries = anim.read(args.anim)
    named_entries = []
    for i in range(len(entries)):
        name = os.path.basename(args.anim)
        name = os.path.splitext(name)[0]
        named_entries.append((f'{name}_{i}.DELT', entries[i]))

    bulkrw.write_files(args.directory, named_entries, False)


def main():
    parser = argparse.ArgumentParser(prog='animtool', description='Tool for Star Wars: Dark Forces ANIM graphics.')
    subparsers = parser.add_subparsers(dest='cmd', required=True, help='the operation to perform')

    # Extract command subparser.
    extract_parser = subparsers.add_parser('extract', help='extract from an LFD')
    extract_parser.set_defaults(func=extract)
    extract_parser.add_argument('anim', help='ANIM to extract from')
    extract_parser.add_argument('directory', help='directory to extract into')


    # Parse arguments.
    args = parser.parse_args()


    # Dispatch command.
    args.func(args)


if __name__ == '__main__':
    main()
