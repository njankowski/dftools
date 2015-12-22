import os


def read_files(directory, recursive):
    # list (filename, data)
    entries = []

    # Recursively read all files.
    if recursive:
        for root, directories, files in os.walk(directory):
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


def write_files(directory, entries, organize):
    # Make top-level.
    os.makedirs(directory, exist_ok=True)

    extensions = set()
    if organize:
        # Collect extensions.
        for entry in entries:
            extensions.add(os.path.splitext(entry[0])[1][1:])
        # Create subdirectories
        for extension in set(extensions):
            try:
                os.makedirs(os.path.join(directory, extension), exist_ok=True)
            except OSError:
                # Remove bad extensions.
                extensions.remove(extension)
                print('Could not make directory "' + extension + '". Files with this extension will be in the top-level directory if possible.')

    # Write files.
    for entry in entries:
        file_extension = os.path.splitext(entry[0])[1][1:]
        if file_extension in extensions:
            file_name = os.path.join(directory, file_extension, entry[0])
        else:
            file_name = file_name = os.path.join(directory, entry[0])
        try:
            with open(file_name, 'wb') as open_file:
                open_file.write(entry[1])
        except OSError:
            print('Bad filename "' + file_name + '". File not written. Continuing...')
