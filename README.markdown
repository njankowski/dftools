# dftools

## What is it?
**dftools** is a suite of Python programs that can be used for working with game assets from:
- Star Wars: Dark Forces (https://en.wikipedia.org/wiki/Star_Wars:_Dark_Forces)
- Outlaws (https://en.wikipedia.org/wiki/Outlaws_(1997_video_game))


## What do I need to use it?
- Python 3.9+ (https://www.python.org/)
- Pillow (https://pypi.org/project/Pillow/)

## Who helped with the project so far?
- njankowski
- Karjala
  - Reported BM examples with broken compression schemes, wrong endianess fields, and zeroed fields
  - Reported GOB example with duplicate entries and non null-terminated names
  - Reported WAX examples with wrong endianess fields
  - Reported GMD example with wrong size field

## What are some examples of assets that I can convert?

Here are some static sprites, animated sprite stills, weapons, and fonts from Dark Forces.

![Jan Ors](examples/jan.png "Jan Ors")
![Stormtrooper Rifle](examples/ist-gunu.png "Stormtrooper Rifle")
![Phase 1 Dark Trooper](examples/phase1.png "Phase 1 Dark Trooper")
![Phase 1 Dark Trooper (GROMAS)](examples/phase1-gromas.png "Phase 1 Dark Trooper (GROMAS)")
![Stormtrooper](examples/stormfin.png "Stormtrooper")
![Stormtrooper Rifle (First Person)](examples/rifle1.png "Stormtrooper Rifle (First Person)")

![Ammo Font](examples/amonum.png "Ammo Font")
![Glowing Font](examples/glowing.png "Glowing Font")

## What are the supported formats?

#### Container
ANIM (ANM), GOB, LFD, LAB

#### Graphics
BM, CMP, DELT (DLT), FME, FNT, NWX, PAL, PLTT (PLT), WAX

#### Sound
GMID, GMD, VOC

#### Level
INF, LEV, LVB, O

#### 3D
VUE

***

## How can I use it?

For detailed information, view the project wiki; otherwise, this quick guide may help you get started.

All tools have a built-in usage guide that can be seen by running the program with no arguments, or with the '-h' or '--help' options.

For example, with the **dfex** program:

`python dfex.py`

`python dfex.py -h`

`python dfex.py --help`

## Quick Examples

It is advised that you do not experiment in your game's installation directory.

Copy the assets elsewhere to be practiced on to avoid destroying your game's install.

### Extract a Container

If you want to explore all of a game's individual files, they are stored in containers.

You can extract all of those individual files to a directory so that they can be inspected individually.

For example, the following command will extract all files in "DARK.GOB" into a directory called "DARK".

`python dfex.py DARK.GOB`

### Create a Container

If you want to repack those same files into a container, you can do that as well.

For example, the following command will create a container called "DARK.GOB" from a directory called "DARK".

`python dfarc.py DARK DARK.GOB`

### Convert a Graphics File (Static Sprite, Texture, or Font Examples)

The tools bmtool, fmetool, and fnttool can be used to convert files of their respective namesakes.

They will convert the image(s) into a PNG (https://en.wikipedia.org/wiki/Portable_Network_Graphics)

For example, the following command will convert all the FME files in "sprites/" to PNGs, and place those PNGs into the same directory.

`python fmetool.py "sprites/*.fme"`

### Convert an Animated Sprite

For example, the following command will convert a single WAX "PHASE1.WAX" into multiple images, and place those PNGs into the same directory.

`python waxtool.py "sprites/PHASE1.WAX"`

## Give me more Dark Forces! (Unaffiliated with this Project)

If you're looking around for Dark Forces stuff, these might interest you.

- https://df-21.net/
- https://twitter.com/DF21net
- https://discord.gg/6T9NvMh2MC (DF-21 Discord)
