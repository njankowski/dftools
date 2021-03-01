import argparse, glob, os, sys
from formats import gob, lab, lfd
from util import bulkrw
from util.vprint import vprint, set_verbose


write_functions = {
    'gob': gob.write,
    'lab': None,
    'lfd': None
}


def do_create(args):
    args.directory = os.path.abspath(args.directory)
    args.container = os.path.abspath(args.container)

    vprint(f'container name "{args.container}"')
    vprint(f'create from directory "{args.directory}"')

    if not os.path.isdir(args.directory):
        sys.exit(f'"{args.directory}" is not a directory to create from.')\

    if not args.force and os.path.isfile(args.container):
        sys.exit(f'Cannot create "{args.container}" because it already exists.\nUse the "-f" or "--force" option to overwrite the container if desired.')

    extension = os.path.splitext(os.path.basename(args.container))[1].lower().lstrip('.')

    if extension not in write_functions:
        sys.exit(f'Unknown container type "{extension}"')

    print(f'Creating "{args.container}" from "{args.directory}"')

    entries = bulkrw.read_files(args.directory, args.recursive)

    write_function = write_functions[extension]
    if write_function:
        vprint(f'calling write function for "{extension}"')
        write_function(args.container, entries)
    else:
        sys.exit(f'Creation for {extension.upper()} containers is not available.')

    print('Done')


def main():
    parser = argparse.ArgumentParser(prog='dfarc', description='Tool for creating Star Wars: Dark Forces and Outlaws containers.')

    parser.add_argument('-f', '--force', help='overwrite existing container files when creating', action='store_true')
    parser.add_argument('-r', '--recursive', help='pack all files in the directory and its subdirectories', action='store_true')
    parser.add_argument('-v', '--verbose', help='print extra information', action='store_true')
    parser.add_argument('directory', help='directory to pack from')
    parser.add_argument('container', help='container to create')

    if len(sys.argv) == 1:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == 'archive':
        sys.argv[1] = 'create'

    args = parser.parse_args()

    set_verbose(args.verbose)

    do_create(args)


if __name__ == '__main__':
    main()
