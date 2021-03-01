import argparse, glob, os
from formats.df import gmd

def from_gmd(args):
    args.file = os.path.abspath(args.file)
    music_files = glob.glob(args.file)
    for music_file in music_files:
        music_name = os.path.splitext(music_file)[0]
        print(f'Converting "{music_name}"')
        tracks = gmd.to_midis(gmd.read(music_file))
        for i in range(len(tracks)):
            track = tracks[i]
            with open(f'{music_name} (Track {i}).mid','wb') as midi_file:
                midi_file.write(bytearray(track))


def main():
    parser = argparse.ArgumentParser(prog='gmdtool',
                                     description='Tool for Star Wars: Dark Forces GMD music.')
    parser.add_argument('file', help='file(s) to convert (as glob)')

    args = parser.parse_args()

    from_gmd(args)


if __name__ == '__main__':
    main()
