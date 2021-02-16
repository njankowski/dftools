"""
Star Wars: Dark Forces run-length encoding functions for paletted images.

RLE0 compresses spans of zero bytes.
RLE1 compresses spans of bytes with any value.

Keep in mind that the "row" being operated on is actually a column of image data.
"""
import struct

NONE = 0
RLE1 = 1
RLE0 = 2


def rle0_decompress(file, width, row_offsets):
    decompressed = []

    for offset in row_offsets:
        file.seek(offset)
        unpacked_bytes = 0
        while unpacked_bytes < width:
            control_byte = struct.unpack("B", file.read(1))[0]
            # Uncompressed bytes.
            if control_byte <= 128:
                decompressed.extend(list(file.read(control_byte)))
                unpacked_bytes += control_byte
            # Expand compressed zero bytes.
            else:
                decompressed.extend([0] * (control_byte - 128))
                unpacked_bytes += control_byte - 128

    if len(decompressed) != width * len(row_offsets):
        raise Exception("decompressed data does not match expected decompressed size")

    return decompressed


def rle0_compress(data, width):
    if (len(data) % width != 0):
        raise Exception("width does not evenly divide data")

    compressed = []
    row_offsets = []

    # Optimize by removing duplicate rows.
    removed_rows, trimmed_data = find_duplicate_rows(data, width)

    index = 0
    while index < len(trimmed_data):
        # Limit compression to the current row.
        # i.e. Do not go into the next row of data in search of bytes to compress.
        zero_bytes = get_contiguous_count(trimmed_data, index, min((index // width) * width + width, len(trimmed_data)), 0)

        # Only compress if there are at least two (zero) bytes to compress.
        if zero_bytes >= 2:
            # Clamp zero bytes.
            if zero_bytes > 127:
                zero_bytes = 127

            compressed.append(zero_bytes + 128)

            # Store the offset to the row if a row boundary is encountered.
            # It is crucial that this action occur after appending the control byte.
            # Offsets must fall on control bytes.
            if index % width == 0:
                row_offsets.append(len(compressed) - 1)

            index += zero_bytes
        # No gainful compression available at the current index. Mark non-compressable bytes.
        else:
            # Get bytes up to first [0, 0] pattern.
            # Limit compression to the current row.
            # i.e. Do not go into the next row of data in search of non-contiguous bytes.
            non_contiguous_bytes = get_non_contiguous_count(trimmed_data, index, min((index // width) * width + width, len(trimmed_data)), 2, [0])

            # Clamp non-contiguous bytes.
            if non_contiguous_bytes > 128:
                non_contiguous_bytes = 128

            compressed.append(non_contiguous_bytes)

            # Store the offset to the row if a row boundary is encountered.
            # It is crucial that this action occur after appending the control byte.
            # Offsets must fall on control bytes.
            if index % width == 0:
                row_offsets.append(len(compressed) - 1)

            compressed.extend(trimmed_data[index : index + non_contiguous_bytes])

            index += non_contiguous_bytes

    # Rebuild offset table.
    if removed_rows:
        # Start with a list of exact length, filled with invalid offsets.
        final_offsets = [-2] * (len(data) // width)

        # Flag child rows.
        for removed in removed_rows:
            final_offsets[removed[1]] = -1

        # Fill parent and non-removed rows.
        parent_offset = 0
        for i in range(len(final_offsets)):
            if final_offsets[i] == -2:
                final_offsets[i] = row_offsets[parent_offset]
                parent_offset += 1

        # Fill child rows.
        for removed in removed_rows:
            final_offsets[removed[1]] = final_offsets[removed[0]]

        row_offsets = final_offsets

    return (compressed, row_offsets)


def rle1_decompress(file, width, row_offsets):
    decompressed = []

    for offset in row_offsets:
        file.seek(offset)
        unpacked_bytes = 0
        while unpacked_bytes < width:
            control_byte = struct.unpack("B", file.read(1))[0]
            # Discard control bytes equal to 128 and the data byte that follows them.
            if control_byte == 128:
                #print(f'bad rle1 control byte {control_byte} at offset {file.tell()}')
                discard = file.read(1)
                #print(f'discarded single data byte {discard}')
                continue
            # Uncompressed bytes.
            if control_byte <= 128:
                decompressed.extend(list(file.read(control_byte)))
                unpacked_bytes += control_byte
            # Expand compressed non-zero bytes.
            else:
                decompressed.extend(list(file.read(1)) * (control_byte - 128))
                unpacked_bytes += control_byte - 128

    if len(decompressed) != width * len(row_offsets):
        raise Exception("decompressed data does not match expected decompressed size")

    return decompressed


def rle1_compress(data, width):
    if (len(data) % width != 0):
        raise Exception("width does not evenly divide data")



    compressed = []
    row_offsets = []

    # Optimize by removing duplicate rows.
    removed_rows, trimmed_data = find_duplicate_rows(data, width)

    index = 0
    while index < len(trimmed_data):
        # Limit compression to the current row.
        # i.e. Do not go into the next row of data in search of bytes to compress.
        contiguous_bytes = get_contiguous_count(trimmed_data, index, min((index // width) * width + width, len(trimmed_data)), trimmed_data[index])

        # Only compress if there are at least three bytes to compress.
        if contiguous_bytes >= 3:
            # Clamp contiguous bytes.
            if (contiguous_bytes > 127):
                contiguous_bytes = 127

            compressed.append(contiguous_bytes + 128)

            # Store the offset to the row if a row boundary is encountered.
            # It is crucial that this action occur after appending the control byte.
            # Offsets must fall on control bytes.
            if index % width == 0:
                row_offsets.append(len(compressed) - 1)

            compressed.append(trimmed_data[index])

            index += contiguous_bytes
        # No gainful compression available at the current index. Mark non-compressable bytes.
        else:
            # Get bytes up to first [n, n, n] pattern.
            non_contiguous_bytes = get_non_contiguous_count(trimmed_data, index, min((index // width) * width + width, len(trimmed_data)), 3)

            # Clamp non-contiguous bytes.
            # Cannot use control byte 128, so the limit is 127.
            if non_contiguous_bytes > 127:
                non_contiguous_bytes = 127

            compressed.append(non_contiguous_bytes)

            # Store the offset to the row if a row boundary is encountered.
            # It is crucial that this action occur after appending the control byte.
            # Offsets must fall on control bytes.
            if index % width == 0:
                row_offsets.append(len(compressed) - 1)

            compressed.extend(trimmed_data[index : index + non_contiguous_bytes])

            index += non_contiguous_bytes

    # Rebuild offset table.
    if removed_rows:
        # Start with a list of exact length, filled with invalid offsets.
        final_offsets = [-2] * (len(data) // width)

        # Flag child rows.
        for removed in removed_rows:
            final_offsets[removed[1]] = -1

        # Fill parent and non-removed rows.
        parent_offset = 0
        for i in range(len(final_offsets)):
            if final_offsets[i] == -2:
                final_offsets[i] = row_offsets[parent_offset]
                parent_offset += 1

        # Fill child rows.
        for removed in removed_rows:
            final_offsets[removed[1]] = final_offsets[removed[0]]

        row_offsets = final_offsets

    return (compressed, row_offsets)


def find_duplicate_rows(data, width):
    height = len(data) // width

    # Split data into rows.
    index = 0
    split_data = [[] for i in range(height)]
    for i in range(height):
        split_data[i].extend(data[index : index + width])
        index += width

    # Find and mark duplicates.
    # List of tuples in the form (parent row, duplicate row).
    removed_rows = []
    for i in range(height):
        # Skip if already marked as duplicate.
        if [item for item in removed_rows if item[1] == i]:
            continue
        for j in range(i + 1, height):
            if split_data[i] == split_data[j]:
                removed_rows.append((i, j))

    # Remove duplicates.
    cleaned_data = []
    for i in range(height):
        # Do not copy data if marked as duplicate.
        if [item for item in removed_rows if item[1] == i]:
            continue
        else:
            cleaned_data.append(split_data[i])

    # Flatten data.
    flattened_data = []
    for row in cleaned_data:
        flattened_data.extend(row)

    return (removed_rows, flattened_data)


def get_contiguous_count(list, start, end, value):
    """
    Gets the number of times that a value repeats in a given interval.

    :param list: The list to analyze.
    :param start: The index to start from. (inclusive)
    :param end: The index to stop at. (exclusive)
    :param value: The value to check for contiguousness.
    :return:
    """
    total = 0
    for index in range(start, end):
        if list[index] == value:
            total += 1
        else:
            break
    return total


def get_non_contiguous_count(list, start, end, contiguous_limit, contiguous_values=[]):
    """
    Gets the number of non-repeating values before a contiguous section in a given interval.

    :param list: The list to analyze.
    :param start: The index to start from. (inclusive)
    :param end: The index to stop at. (exclusive)
    :param contiguous_limit: How many times a value must appear before being considered a contiguous section.
    :param contiguous_values: Values to look for contiguousness of. If empty, all values are analyzed.
    e.g. If looking for contiguous zeroes only, make contiguous_values = [0]. When a contiguous string of zeroes
    are found matching the contiguous_limit, the search terminates.
    :return: Number of non-contiguous values before a contiguous section.
    """
    total = 0
    index = start
    while index < end:
        if contiguous_values:
            if list[index] in contiguous_values:
                contiguous = get_contiguous_count(list, index, end, list[index])
            else:
                contiguous = 1
        else:
            contiguous = get_contiguous_count(list, index, end, list[index])

        if contiguous < contiguous_limit:
            total += contiguous
        else:
            break
        index += contiguous
    return total

def calc_ideal_compression_fme(data, width):
    uncompressed = len(data)
    rle0 = len(rle0_compress(data, width)[0])
    # In order of preference.
    if uncompressed <= rle0:
        return NONE
    else:
        return RLE0

def calc_ideal_compression_bm(data, width):
    uncompressed = len(data)
    rle0 = len(rle0_compress(data, width)[0])
    rle1 = len(rle1_compress(data, width)[0])

    # In order of preference.
    if (uncompressed <= rle0 and uncompressed <= rle1):
        return NONE
    if (rle0 <= uncompressed and rle0 <= rle1):
        return RLE0
    if (rle1 <= uncompressed and rle1 <= rle0):
        return RLE1
