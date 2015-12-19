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


def write_files(directory, entries):
    for entry in entries:
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, entry[0])
        with open(file_name, 'wb') as open_file:
            open_file.write(entry[1])
