import argparse
import glob
import os
from formats import gmd


args = None


def convert_gmd():
    music_files = glob.glob(args.file)
    for music_file in music_files:
        music_name = os.path.splitext(music_file)[0]
        print('Converting "' + music_name + '"')
        tracks = gmd.to_midis(gmd.read(music_file))
        for i in range(len(tracks)):
            track = tracks[i]
            with open('{music_name} (Track {track_number}).mid'.format(music_name=music_name, track_number=i),'wb') as midi_file:
                midi_file.write(bytearray(track))

    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gmdtool',
                                     description='Tool for Star Wars: Dark Forces GMD music.')
    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    convert_gmd()
