# dftools
Tools for Star Wars: Dark Forces assets.

### First Off...
***Be careful with these tools! At present, these tools will overwrite any files in a directory with identical names when writing files!***

### Requirements
* Python 3
* Pillow (PIL Fork)

### Examples

![Jan Ors](examples/jan.png "Jan Ors")
![Stormtrooper Rifle](examples/ist-gunu.png "Stormtrooper Rifle")

*Converted from FME to PNG with fmetool.*

***

### Supported Formats

#### Containers
* GOB (Asset Archive)

#### Graphics
* BM (Textures, Weapons)
* CMP (Colormap)
* FME (Static Sprites)
* FNT (Bitmap Fonts)
* PAL (Color Palette)
* WAX (Animated Sprites)

#### Sound
* GMD (Custom MIDI Format 2)

***

### How To

#### gobtool
**Extract a GOB**

*There are some GOBs out there with bad filenames archived inside (e.x. the Dark Forces demo). The tool will print a warning if it tried to write a file but could not.*

`python gobtool.py extract "DARK.GOB" "DARK"`

*Extracts a GOB named "DARK.GOB" in the current directory, to a folder "DARK" in the current directory.*

*Will automatically create directories that do not exist.*

`python gobtool.py extract -o "DARK.GOB" "DARK"`

`python gobtool.py extract --organize "DARK.GOB" "DARK"`


*Extracts a GOB named "DARK.GOB" in the current directory, to a folder "DARK" in the current directory.*

*Will create a subdirectory (within the specified directory) for each file extension in the archive. Will place each file into the appropriate subdirectory.*

**Make a GOB**

`python gobtool.py archive "CUSTOM.GOB" "CUSTOM"`

*Archives all of the files in folder "CUSTOM" (top-level only) in the current directory, to a GOB named "CUSTOM.GOB" in the current directory.*

`python gobtool.py archive -r "CUSTOM.GOB" "CUSTOM"`

`python gobtool.py archive --recursive "CUSTOM.GOB" "CUSTOM"`

*Archives all of the files in folder "CUSTOM" (including subdirectories) in the current directory, to a GOB named "CUSTOM.GOB" in the current directory.*

*Allows files to remain organized before packing.*

#### fmetool
**Convert an FME**

*PNG only.*

*Tool uses glob (e.x. wildcard) patterns for file(s) specification.*

`python fmetool.py "sprites/*.fme"`

*Converts all FME files in the sprites directory to "filename.png" using default palette SECBASE.*

*Writes converted files into the same directory."*

`python fmetool.py -p JABSHIP "sprites/JAN.fme"`

*Converts a single FME "JAN.FME" in the sprites directory to "JAN.png" using built-in palette JABSHIP.*

`python fmetool.py -p "palettes/custom.pal" "sprites/JAN.fme"`

*Converts a single FME "JAN.FME" in the sprites directory to "JAN.png" using external palette "palettes/custom.pal".*

**Make an FME**

*Not supported.*