import argparse
from formats import gob
from util import bulkrw


args = None


def archive_gob():
    print('Archiving "' + args.directory + '" into GOB "' + args.gob + '"')

    entries = bulkrw.read_files(args.directory, args.recursive)
    gob.write(args.gob, entries)

    print('Done')


def extract_gob():
    print('Extracting "' + args.gob + '" into directory "' + args.directory + '"')

    entries = gob.read(args.gob)
    bad_entries = bulkrw.write_files(args.directory, entries, args.organize)

    if args.interactive and bad_entries:
        print('Some files could not be saved. Please provide a name for each file when prompted.')
        bulkrw.rename_and_write_files_interactive(args.directory, bad_entries)
    elif bad_entries:
        print('Some files could not be saved. Use the "-i" or "--interactive" option to extract these files.')

    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gobtool',
                                     description='Tool for Star Wars: Dark Forces GOB archives.')

    parser.add_argument('-r', '--recursive',
                        help='archive all files in the directory and its subdirectories (archive mode only)',
                        action='store_true')
    parser.add_argument('-o', '--organize',
                        help='create a subdirectory for each file extension in the archive (extract mode only)',
                        action='store_true')
    parser.add_argument('-i', '--interactive',
                        help='manual renaming when extracting files with bad filenames',
                        action='store_true')

    parser.add_argument('mode', choices=['archive', 'extract'],
                        help='mode of operation')
    parser.add_argument('gob', help='GOB to extract from / archive to')
    parser.add_argument('directory', help='directory to extract to / archive from')

    args = parser.parse_args()

    if args.mode == 'archive':
        archive_gob()
    elif args.mode == 'extract':
        extract_gob()
