"""
Seems like GMD is a MIDI format 2 file with an extra 8 bytes at the beginning.
There are multiple tracks within the GMD, and they are played independently by iMUSE.
I suppose the goal is to extract each track and place it into its own MIDI format 0 file
for maximum playability.
"""
import struct

class MidiChunk:
    def __init__(self):
        self.type = b''
        self.size = 0
        self.raw_data = b''

class Gmd:
    def __init__(self):
        self.size = 0

        self.midi_chunks = []

def read(filename):
    with open(filename, 'rb') as file:
        gmd = Gmd()

        file.seek(0, 2)
        end_offset = file.tell()
        file.seek(0)

        # extra imuse header
        if file.read(4) != b'MIDI':
            raise Exception('File has no GMD magic identifier.')

        gmd.size = struct.unpack('>i', file.read(4))[0]

        # Fix the GMD size if it erroneously equals the whole file size.
        # Let correct or any other strange size values fall through untouched.
        if gmd.size == end_offset:
            print('gmd size fixup applied')
            gmd.size = end_offset - 8

        bytes_read = 0
        while bytes_read < gmd.size:
            midi_chunk = MidiChunk()
            midi_chunk.type = file.read(4)
            midi_chunk.size = struct.unpack('>i', file.read(4))[0]
            midi_chunk.raw_data = file.read(midi_chunk.size)
            bytes_read += midi_chunk.size + 8

            # Only want standard MIDI chunks.
            if midi_chunk.type == b'MThd' or midi_chunk.type == b'MTrk':
                gmd.midi_chunks.append(midi_chunk)

        return gmd

def to_midis(gmd):
    midis = []
    header = [chunk for chunk in gmd.midi_chunks if chunk.type == b'MThd'][0]
    for chunk in gmd.midi_chunks:
        if chunk.type == b'MThd':
            continue
        midi = []
        midi.extend(list(header.type))
        midi.extend(list(struct.pack('>i', header.size)))
        midi.extend(list(struct.pack('>hh', 0, 1)))
        midi.extend(list(header.raw_data[4:6]))
        midi.extend(list(chunk.type))
        midi.extend(list(struct.pack('>i', chunk.size)))
        midi.extend(list(chunk.raw_data))
        midis.append(midi)
    return midis
