import os
from collections import Counter


def read_files(directory, recursive):
    """Read all files in a directory."""
    # (filename, data)
    entries = []

    # Get absolute path, just in case working directory changes.
    directory = os.path.abspath(directory)

    # Recursively read all files.
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                with open(os.path.join(root, file), 'rb') as open_file:
                    entries.append((file, open_file.read()))
    # Read top-level only.
    else:
        for file in os.listdir(directory):
            file_name = os.path.join(directory, file)
            if os.path.isfile(file_name):
                with open(file_name, 'rb') as open_file:
                    entries.append((file, open_file.read()))

    return entries


def write_files(directory, entries, organize, overwrite):
    """Write a list of files to a directory.

    :param directory: The directory to write the files to
    :param entries: List of file tuples [(str, bytes), ..., ] where the tuple represents (name, data) of the file
    :param organize: If True, create a directory for each file type and place files of that type there
    :param overwrite: If True, allow directories and files to be overwritten
    :return: List of file tuples that could not be written, if any
    """
    # (filename, data)
    bad_entries = []

    # Get absolute path.
    directory = os.path.abspath(directory)

    # Make top-level.
    if os.path.isdir(directory) and not overwrite:
        print(f'Directory "{directory}" already exists. Aborting.')
        return
    else:
        os.makedirs(directory, exist_ok=True)

    # Append number to duplicate files.
    filename_counts = Counter([name for (name, data) in entries])
    duplicate_files = [name for name, count in filename_counts.items() if count > 1]

    for filename in duplicate_files:
        value = 0
        for i, entry in enumerate(entries):
            if entry[0] == filename:
                new_name = os.path.splitext(filename)[0] + f'-{value}' + os.path.splitext(filename)[1]
                entries[i] = (new_name, entry[1])
                value += 1
                print(f'Duplicate filename "{filename}" renamed to "{new_name}"')

    # Prepare extensions for translation into directories.
    extensions = set()
    if organize:
        # Collect extensions.
        for entry in entries:
            extensions.add(os.path.splitext(entry[0])[1][1:])
        # Create subdirectories.
        for extension in set(extensions):
            try:
                if os.path.isdir(directory) and not overwrite:
                    print(f'Directory "{directory}" already exists. Aborting.')
                    return
                else:
                    os.makedirs(os.path.join(directory, extension), exist_ok=True)
            except OSError:
                # Remove bad extensions.
                extensions.remove(extension)
                print(f'Could not make directory "{extension}"')
                print('Files with this extension will be in the top-level directory if possible.')

    # Write files.
    for entry in entries:
        file_extension = os.path.splitext(entry[0])[1][1:]
        if file_extension in extensions:
            file_name = os.path.join(directory, file_extension, entry[0])
        else:
            file_name = os.path.join(directory, entry[0])
        try:
            if os.path.isfile(file_name) and not overwrite:
                print(f'File "{file_name}" already exists. File not overwritten.')
            with open(file_name, 'wb') as open_file:
                open_file.write(entry[1])
        except OSError:
            bad_entries.append(entry)
            print(f'Bad filename "{file_name}". File not written.')

    return bad_entries


def write_files_interactive(directory, entries):
    """Write a list of file entries to a directory, with interactive renaming."""
    # Nothing to write if entries are empty.
    if not entries:
        return

    # Get absolute path, just in case working directory changes.
    directory = os.path.abspath(directory)

    # Initial prompt.
    print('Type "s" to skip saving a file, or "q" to quit.')

    # Loop through entries, prompting for action.
    i = 0
    while i < len(entries):
        entry = entries[i]
        new_filename = input('"' + entry[0] + '" -> ')
        # Skip entry.
        if new_filename.strip().lower() == 's':
            print('Skipped renaming of file "' + entry[0] + '"')
            i += 1
            continue
        # Quit
        elif new_filename.strip().lower() == 'q':
            break
        # Rename entry.
        else:
            try:
                new_filename = os.path.join(directory, new_filename)
                # Check if a file with that name already exists.
                if os.path.isfile(new_filename):
                    print('A file with that name already exists in the top-level directory.')
                    print('"r" to rename again. "o" to overwrite. "s" to skip. "q" to quit.')
                    choice = input().strip().lower()
                    # Skip
                    if choice == 's':
                        print('Skipped renaming of file "' + entry[0] + '"')
                        i += 1
                        continue
                    # Rename entry again.
                    elif choice == 'r':
                        continue
                    # Quit
                    elif choice == 'q':
                        break
                # Write file.
                with open(new_filename, 'wb') as open_file:
                    open_file.write(entry[1])
                print('Wrote renamed file to "' + new_filename + '"')
            # Still a bad filename.
            except OSError:
                print('Bad filename. Please try again.')
            # Successfully wrote file.
            else:
                i += 1
