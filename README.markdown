# dftools
Tools for Star Wars: Dark Forces assets.

### First Off...
***Be careful with these tools! At present, these tools will overwrite any files in a directory with identical names when writing files!***

### Requirements
* Python 3.6 or greater
* Pillow (PIL Fork)

### Examples

**fmetool**

![Jan Ors](examples/jan.png "Jan Ors")

*Jan Ors*

![Stormtrooper Rifle](examples/ist-gunu.png "Stormtrooper Rifle")

*Stormtrooper Rifle*

**waxtool**

![Phase 1 Dark Trooper](examples/phase1.png "Phase 1 Dark Trooper")
![Phase 1 Dark Trooper (GROMAS)](examples/phase1-gromas.png "Phase 1 Dark Trooper (GROMAS)")

*Phase 1 Dark Trooper (Right-side has GROMAS color palette for that extra spooky red tinge!)*

![Stormtrooper](examples/stormfin.png "Stormtrooper")

*Stormtrooper*

**bmtool**

![Stormtrooper Rifle (First Person)](examples/rifle1.png "Stormtrooper Rifle (First Person)")

*Stormtrooper Rifle (First Person)*

**fnttool**

![Ammo Font](examples/amonum.png "Ammo Font")

*Ammo Font*

![Glowing Font](examples/glowing.png "Glowing Font")

*Glowing Font*

***

### Supported Formats

#### Containers
* GOB (Asset Archive)
* LAB (Asset Archive for Outlaws)

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

#### labtool (Outlaws)
**Extract a LAB**

`python labtool.py extract "OUTLAWS.LAB" "OUTLAWS"`

*Extracts a LAB named "OUTLAWS.LAB" in the current directory, to a folder "OUTLAWS" in the current directory.*

*Will automatically create directories that do not exist.*

`python labtool.py extract -o "OUTLAWS.LAB" "OUTLAWS"`

`python labtool.py extract --organize "OUTLAWS.LAB" "OUTLAWS"`


*Extracts a LAB named "OUTLAWS.LAB" in the current directory, to a folder "OUTLAWS" in the current directory.*

*Will create a subdirectory (within the specified directory) for each file extension in the archive. Will place each file into the appropriate subdirectory.*

#### fmetool
**Convert an FME**

*PNG only.*

*Tool uses glob (e.x. wildcard) patterns for file(s) specification.*

*Writes converted files into the same directory."*

`python fmetool.py "sprites/*.fme"`

*Converts all FME files in the sprites directory to "filename.png" using default palette SECBASE.*

`python fmetool.py -p JABSHIP "sprites/JAN.fme"`

*Converts a single FME "JAN.FME" in the sprites directory to "JAN.png" using built-in palette JABSHIP.*

`python fmetool.py -p "palettes/custom.pal" "sprites/JAN.fme"`

*Converts a single FME "JAN.FME" in the sprites directory to "JAN.png" using external palette "palettes/custom.pal".*

**Make an FME**

*Not supported.*

#### waxtool
**Convert a WAX**

*PNG only.*

*Images are auto-labeled based on sprite state.*

*Only can convert one WAX at a time. Make sure to gather converted files before continuing use.*

*Writes converted files into the same directory.*

*Palette can be specified, much like fmetool.*

`python waxtool.py "sprites/PHASE1.WAX"`

*Converts a single WAX "PHASE1.WAX" into multiple images.*


**Make a WAX**

*Not supported.*

#### bmtool

*Refer to fmetool. Its operation is identical, except that bmtool may generate multiple image files per BM.*

#### fnttool

*Refer to fmetool. Its operation is identical.*
