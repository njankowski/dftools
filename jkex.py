import argparse, glob, os, pathlib, sys
from formats.jk import gob
from util.vprint import vprint, set_verbose


read_functions = {
    'gob': gob.read,
}


def do_extract(args):
    args.container = os.path.abspath(args.container)

    if args.directory:
        args.directory = os.path.abspath(args.directory)
        vprint(f'extract directory specified as "{args.directory}"')
    else:
        args.directory = os.path.dirname(args.container)
        vprint(f'extract directory not specified')
        vprint(f'setting extract directory to "{args.directory}"')

    containers = glob.glob(args.container)

    vprint(f'{len(containers)} containers in glob')

    for container in containers:
        vprint(f'extracting "{container}"')
        container_name = os.path.splitext(os.path.basename(container))[0]
        extract_directory = os.path.join(args.directory, container_name)

        vprint(f'container name "{container_name}"')
        vprint(f'container extract directory "{extract_directory}"')

        if not os.path.isfile(container):
            sys.exit(f'"{container}" is not a container file to extract from.')

        if not args.force and os.path.isdir(extract_directory):
            sys.exit(f'Cannot extract to "{extract_directory}" because it already exists.\nUse the "-f" or "--force" option to overwrite the directory if desired.')

        extension = os.path.splitext(os.path.basename(container))[1].lower().lstrip('.')
        vprint(f'extension resolved to "{extension}"')

        if extension not in read_functions:
            sys.exit(f'Unknown container type "{extension}"')

        print(f'Extracting "{container}" into "{extract_directory}"')

        read_function = read_functions[extension]
        if read_function:
            vprint(f'calling read function for "{extension}"')
            entries = read_function(container)
        else:
            sys.exit(f'Extraction for {extension.upper()} containers is not available.')

        os.makedirs(extract_directory, exist_ok=True)

        for entry in entries:
            name, ext = os.path.splitext(os.path.basename(entry[0]))
            entry_path = os.path.dirname(entry[0])
            full_path = os.path.join(extract_directory, entry_path)
            pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(full_path, name + ext), 'wb') as f:
                f.write(entry[1])


    print('Done')


def main():
    parser = argparse.ArgumentParser(prog='dfex', description='Tool for extracting Star Wars Jedi Knight: Dark Forces 2 GOB containers.')

    parser.add_argument('-d', '--directory', help='directory to extract the specified containers into')
    parser.add_argument('-f', '--force', help='overwrite existing directories and files when extracting', action='store_true')
    #parser.add_argument('-i', '--interactive', help='manual renaming when extracting files with bad filenames', action='store_true')
    #parser.add_argument('-o', '--organize', help='create a subdirectory for each file extension in the container', action='store_true')
    parser.add_argument('-v', '--verbose', help='print extra information', action='store_true')
    parser.add_argument('container', help='containers to extract from as glob')

    if len(sys.argv) == 1:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    set_verbose(args.verbose)

    do_extract(args)


if __name__ == '__main__':
    main()
