import argparse
from formats import gob
from util import bulkrw


args = None


def archive_gob():
    print("Archiving \"" + args.directory + "\" into GOB \"" + args.gob + "\"")

    entries = bulkrw.read_files(args.directory, args.recursive)
    gob.write(args.gob, entries)

    print("Done")


def extract_gob():
    print("Extracting \"" + args.gob + "\" into directory \"" +
          args.directory + "\"")

    entries = gob.read(args.gob)
    bulkrw.write_files(args.directory, entries, args.organize)

    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="gobtool",
                                     description="Tool for Star Wars: Dark Forces GOB archives.")

    parser.add_argument("-r", "--recursive",
                        help="archive all files in the directory and its subdirectories (archive mode only)",
                        action="store_true")
    parser.add_argument("-o", "--organize",
                        help="create a subdirectory for each file extension in the archive (extract mode only)",
                        action="store_true")

    parser.add_argument("mode", choices=["archive", "extract"],
                        help="mode of operation")
    parser.add_argument("gob", help="GOB to extract from / archive to")
    parser.add_argument("directory", help="directory to extract to / archive from")

    args = parser.parse_args()

    if args.mode == "archive":
        archive_gob()
    elif args.mode == "extract":
        extract_gob()
