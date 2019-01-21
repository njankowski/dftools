"""
Star Wars Dark: Forces color palette functions.

A Dark Forces color palette is a VGA Mode 13h palette.

VGA Mode 13h is limited to 256 colors at 6-bits per channel, so each
channel ranges from 0-63 inclusive.

Dark Forces treats color 0 as transparent (under most conditions). All others are opaque.
"""
import struct
from util import imaging
import base64


# The number of colors present in a palette.
NUM_COLORS = 256

# The number of channels per color. (RGB)
NUM_CHANNELS = 3

# The palette color that represents transparency.
TRANSPARENT_COLOR = 0


def read(filename):
    palette = []

    with open(filename, "rb") as file:
        for color in range(NUM_COLORS):
            r = struct.unpack("B", file.read(1))[0]
            g = struct.unpack("B", file.read(1))[0]
            b = struct.unpack("B", file.read(1))[0]
            palette.append((r, g, b))

    return palette


def write(filename, palette):
    with open(filename, "wb") as file:
        for color in range(NUM_COLORS):
            file.write(struct.pack("B", palette[color][0]))
            file.write(struct.pack("B", palette[color][1]))
            file.write(struct.pack("B", palette[color][2]))


def is_vga13h_palette(palette):
    # 256 colors.
    if len(palette) != NUM_COLORS:
        return False

    for color in range(NUM_COLORS):
        # RGB
        if len(palette[color]) != NUM_CHANNELS:
            return False
        # VGA Mode 13h. 6-bits per channel.
        if not ((0 <= palette[color][0] < 2 ** 6) and
                (0 <= palette[color][1] < 2 ** 6) and
                (0 <= palette[color][2] < 2 ** 6)):
            return False

    return True


def vga13h_to_rgb(palette):
    rgb_palette = []

    for color in range(NUM_COLORS):
        rgb_palette.append(((palette[color][0] << 2) | (palette[color][0] >> 4),
                            (palette[color][1] << 2) | (palette[color][1] >> 4),
                            (palette[color][2] << 2) | (palette[color][2] >> 4)))

    return rgb_palette


def rgb_to_vga13h(rgb_palette):
    palette = []

    for color in range(NUM_COLORS):
        palette.append(((rgb_palette[color][0] >> 2),
                        (rgb_palette[color][1] >> 2),
                        (rgb_palette[color][2] >> 2)))

    return palette


def to_image(rgb_palette):
    from PIL import Image
    image = imaging.to_image(list(range(0,256)), 256, 1, rgb_palette, True)
    return image


def load_internal(name):
    decoded = base64.b64decode(default_palettes[name])

    palette = []

    for i in range(NUM_COLORS):
        r = decoded[(i * 3) + 0]
        g = decoded[(i * 3) + 1]
        b = decoded[(i * 3) + 2]
        palette.append((r, g, b))

    return vga13h_to_rgb(palette)


ARC = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


BUYIT = \
'AAAAAAAAIw4SJxAWEAQIEgAIHhQcBAIEEA4QCAAQCggQAAArAAAxAAA1BAQlBAQeBAQOFB\
QcCAoUAAIKCAoQAAQOFBYaISMnHiElCgoKAAoUEhYaBgoOCg4QEhYYGh4hEBQWGBweDhIU\
FBgaFhocDBIUGiEjAggIBggIBgwKBgoIBAoGAgIABAQCPz0rPzspCAYAJyEQCggEIxwOJR\
4QBgQADAgAEAwEPTMePzktGhIEKSESFA4EIxwSFg4CGBAEIRgMPTEeCgYAEAoCJRgIIRYI\
JxoKIxgKLSEQLyMSKyESNysaPzMjPzUnFAwCGhAEFg4EHBIGJRoOIRgOOy0aPS8cPzMlPz\
UpLyEQMSMSMyUUNScWKR4SNykYOSsaPzEhEgoCHBAEGhAGKRoMLx4OKxwOLR4QPS0cNyka\
Py8eNSkcPzEjJRwUPTElHhgSKyMaFhIOJyMeDAYAOSUSOycUPysYPy0cGBQQJRQGHBAGLx\
oKKRgKPSUQOSMQIRQKPScUKxwQOScWPSkYPysaCAgILxgIPSMOOSEOFAwGMR4QOycWPy0e\
DgYAMRYEHA4ENRoINxwKMxoKHhIKHhYQCgQAKxQGNRoKGg4GJRQKNR4QPykaIQ4EKRIGIx\
AGMRQGLxQGHAwEMxYIPyUWMRwSIRQOGBAMGhIOLQ4AIwwCLRIGIQ4GOxoMOxwOKxgQHBQQ\
KSkpMRIGKxIIOxwQPR4SPyEUDgQAEAYCNxoQNxwSJRQOKRgSKRAINRYMNxgOLRQMOxoQJR\
IMMRgQFA4MGhQSMRQMMRYOKRIMHhAMMRIKHAwILRQOFg4MHgwIGhAOFAoIHBIQGgwKGg4M\
JRQSKQYEDAAAFgAAHAAAIQAAJQAAKwAAMwAAPwAAFAYGEAYGFggICgQEFAgIHg4OIRAQIx\
ISJxYWKRgYHhISKRoaBgQELR4eLyEhMSMjHBQUDgoKLyMjMycnIxoaNSsrOTExDgwMIRwc\
NS8vGhgYOzc3HBoaIyEhJyUlLy0tMzExNzU1FhYWPz8/'


DTENTION = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


EXECUTOR = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


FUELSTAT = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


GROMAS = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ozc2OTQzNzAv\
NS0sNCwrMikoMSYlLyMiLSEfLB8eKh0bKBoZJhgWJRcVIxUTIRIRHxAPHg8OHA4MGw0LGQ\
sKGAoJFgkHFQgHEwYFEgYFEAUEDwQDDQMCDAICCgIBCQEBGw4TGQ0QFwsOFQkMFAgKEgYI\
EAYHDwUFDQMECwIDCQICCAEBBgABAwAAAgAAAAAAPzUgPC0ZOCcTNSIPMR0KLxgHKxUFJx\
ADJA0CIAoBHQgAGQYAFQQAEgIADgEACwEAOQ4ANg0AMwsAMQoALgkALAcAKQYAJgUAIwUA\
IAQAHgMAGwIAGAIAFQEAEgEAEAEAIjULHi8IGyoFGSYEFiICEx4BERkBDxYADRIACw8ACg\
0ADgkAEAcAEAUADQIACgEAPy8pPikiPSUcOyEXOR0TOBkPNhYMNRMKMxAHMg4FMQ0DMAsC\
LgkBLQkAKwcAKgYAJwsAJAgAIQUAHgMAHAIAGQEAFgAAFAAAAAA/AAAzAAApAAAgAAAXAA\
ARAAALAAAHPwAAOQAAMgAALAAAJQAAHgAAFwAAEAAAPxMAOQ4AMwsALggAKAUAIgMAHAIA\
FgEAMQ8FLw4ELAwEKQoDJwkDJAgCIQYBHwYBHAUBGQMBFgMAFAIAEQIADgEADAEAEQIAMD\
c/LDQ+KTI+JS88Iiw6Hyk6Gyc4GCU4FSI2EiE2Dx41DBs1CRkzBhczAhYxABMxPxoAPRgA\
OxcAORYANxUANRQAMxIAMREALxABLQ8BKw4BKQ0BJwwBJQwBIwsBIQoBHwkBHggBHAcBGg\
YAGQUAFwQAFgMAFAIAEwIAEQEADwEADgAADAAACwAACQAACAAAMSYmLiIiLB8fKhwcKBkZ\
JhcXIxQUIRISHw8PHQ0NGgsLGAkJFggIFAYGEgUFPz8/'


IMPCITY = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


JABSHIP = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3PzYOPTMN\
OzAMOS0LNyoKNScJMyUJMiIIMCAHLh0HLBsGKhkFKBYFJhQEJBIDIxADIQ4CHw0CHQsCGw\
kBGQgBFwYBFQUBFAQAEgMAEAIADgEADAEACgAACAAABgAABQAAAAAAJxoSPz43LCkmIR8b\
GxsSFhYOERELDAwHCwgBCAIBBQUEGA8GIhIFKhUGPz8/'


NARSHADA = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAALwAAIAAAEQAAAD8AADIAACYAABkAAA0AABY/AA01AA\
YsAAEjPjgYPS4NPSIDNhYDLQsBFB0uEhsrERkoEBcmDhUjDRMhDBEeCxAcOjo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
Dg8TDQ0RCwsPCQoMBwgKBgYIBAQGAgIDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZIDUXIDIVHy8THywRHigQHSUOHCINGx4LGRsKFx\
gIFRQHERAFDgwECwkDCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoQKxkOKBcNJRUMIxQLIBIKHhAJGw8IGQ0HFgwGFAsFEQkEDwcDDAYCCgUCLj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GSEbFx4Z\
FRwXExoVEhgTEBURDhMQDREOCw8MCQwKBwoIBggGBAYEAgMDAQEBAAAAPz8/OTo7NDU3Lz\
AzKisvJScrISMnHR8kPy4AOCYAMh8ALBgAJhMAIA0AGgkAFAYAJAAAIQAAHwAAHQAAGgAA\
GAAAFQAAEwAAEQAADgAADAAACgAABwAABQAAAwAAPz8/'


RAMSHED = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


ROBOTICS = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3OT09NTs7\
Mjk5Ljc4KzY2KDQ0JTIzIjAxHy8vHS0uGissFykqFScpEyUnESQlDyIkDR8iCx0gChoeCB\
gcBxYaBRMYBBEWAw8UAg0SAQsQAQkOAQcMAAYKAAQIAAMHAAIFPT4+Oz09OD09Nzw9NDs8\
Mzs8MDo7Lzk7LTg7Kzc6KTY6JzU6JTQ5IzM5IjI5Pz8/'


SECBASE = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


SEWERS = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAALwAAIAAAEQAAAD8AADIAACYAABkAAA0AABY/AA01AA\
YsAAEjPzgAOioANh4AMRMBLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NTU1MzMzMTExMDAwLi4uLCwsKysrKSkpKCgoJiYmJCQkIyMjISEhHx8fHh4eHBwcGhoaGR\
kZFxcXFRUVFBQUEhISEBAQDw8PDQ0NDAwMCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoQKxkOKBcNJRUMIxQLIBIKHhAJGw8IGQ0HFgwGFAsFEQkEDwcDDAYCCgUCPz\
8/Ojw+NTo+MDg9LDY8JzM8IzE7Hy87Gi06Fis6Eik5Dic5CiU4BiM4AiE3ACA3GSgAGiUA\
GiMAGyEAGx8AGx0AGxsAGRcAFxQAFBAAEg4AEAsADggADAYACgQACAMAABgzABMxABAwAA\
wvAAguAAUtAAIsAAArMDA/Kio6JCU1HyAxGxwsFhgoEhQjDxEfAAA/AAA6AAA2AAAxAAAs\
AAAoAAAjAAAfAAAaAAAWAAARAAANAAAIAAADAAAAPz8/'


TALAY = \
'AAAAPz8/NDs/KTc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABkAAA0AABY/AA01AA\
YsAAEjPzgAOioANh4AMRMBLQsBGh0uFxsrFRkoExcmEBUjDhMhDBEeCxAcOjo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dGxsbGhoaGBgYFx\
cXFRUVFBQUEhISERERDw8PDg4ODAwMCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoQKxkOKBcNJRUMIxQLIBIKHhAJGw8IGQ0HFgwGFAsFEQkEDwcDDAYCCgUCLj\
o/Kjg+Jzc+IzU9IDM8HTI8GTA7Fi47Ey06ECs6DSk5Cig5ByY4BCQ4ASI3ACE3AB41ABgz\
ABQyAA8wAAovAAYtAAIsAAArMDA/LCw7KCg4JCU0ICIxHR4tGhwqFxknPzI/Ois7NCU3Ly\
AzKRsvJBYrHhInGQ4jEwofDwcbCgUXBwMTBQIRBAEQAwEOAgENAgELAQAKAQAIAAAHAAAG\
AAAEAAADAAA/AAA2AAAsAAAjAAAaAAARAAAIAAAAPz8/'


TESTBASE = \
'AAAAPz8/NDs/Kjc/HzM/FTA/PwAAMwAAJAAAEQAAAD8AADIAACYAABcAAA0AABY/AAk8AA\
QvAAEjPjgYPS4NPSIDNhYDLQsBPwA/PwA/PwA/PwA/PwA/PwA/PwA/PwA/Ojo6ODg4NjY2\
NDQ0MzMzMTExLy8vLS0tKysrKioqKCgoJiYmJCQkIyMjISEhHx8fHR0dHBwcGhoaGRkZFx\
cXFhYWFBQUExMTEREREBAQDg4ODQ0NCwsLCgoKCAgIBwcHGRshFxkeFRccExUaEhMYEBEV\
DhATDQ4RCwwPCQoMBwgKBgYIBAQGAgMDAQEBAAAAPzksOzQmNzAhNCwdMCgYLSQUKSERJR\
0NIhkKHhYHGxMFFxADEw0CEAoBDAcACQUAOBsDNRkCMhcCLxYBLBQBKhIBJxEBJA8BIQ4A\
Hg0AHAsAGQoAFggAEwcAEAYADgUAIDkZHDUVGTIRFy8OFCwLESkIDyUGDSIDCx8CCRwACB\
kADBUBDhIBDg4CCwoCCAYCPzUyPTEtPC4pOislOCghNyUdNSIaNCAXMh0TMRsQLxkNLhcK\
LBUIKxQFKRIDKBEBJRcAIhMAHw8AHAwAGgkAFwcAFAQAEgMAAAA/AAA4AAAyAAAsAAAlAA\
AfAAAZAAATPwAAOAAAMQAAKgAAIwAAHAAAFQAADgAAPyAAOBsAMhcALBMAJg8AIAsAGggA\
FAYAMBwRLRoPKhgOJxYNJRUMIhMLHxEJHRAIGg4HFwwGFAsFEgkEDwgDDAYCCgUCDwgELj\
o/Kjg+Jzc+IzU9IDM8HTE8GTA7Fi47Eyw6ECs6DSk5Cic5ByU4BCM4ASI3ACA3GRshGBog\
FxkeFhgdFRccFBYbFBUaExQZEhMYERMXEBIWDxEVDxAUDg8SDQ4RDA0QCwwPCgsOCgsNCQ\
oMCAkLBwgKBgcJBgYIBQUGBAQFAwMEAgIDAQICAQEBAAAAAAAAAAAkAAAhAAAeAAAcAAAZ\
AAAWAAAUAAARAAAPAAAMAAAJAAAHAAAEAAABAAAAPz8/'


WAIT = \
'AAAAOTk5NzU1MzMxMTEvMS8tLy8tLy0rLSsrLSspKyspLSknKScnMSMhKSclNSEeKycjJy\
clKSUhJyUjIyMjJSMhJyMeLR4cKx4cKR4eISEjLRwaJSEcIyEeJx4cIyEcISEeKxoaKRoa\
Ix4cKxgYJxoaIx4aJRwaLRgWHh4eIxwaJxoYIR4aHh4cHBweHhwcKxYWIRwYIRoYJRgWGB\
oeHBoaKRQUHhoYHBoYIRgWJRYUHhoWGhoYKRISJxQSHBoWIxYUGhgYIRYUHhgUHhYWGBgY\
HBgUIxQSFhYcGhgUGBgWJRIQJxAQHBYUHhQUIxIQGhgSFhYYGhYUHhQSIRIQGBYUFBQaGh\
QUGhYSHhIQGBYSGhQSIxAOJQ4OFhYUFBYWGhQQEhIaGBQSHBIQIRAOFBQWBhwcFhQUIRAM\
GhIQCBoaEhQWFBQUFhQSBhoaFBQSIQ4MGhIOFhISFhQQHBAOCBgYFBISFhIQHBAMGhAOEh\
IUGBIODhYUHg4MFBIQEhISEBIUBhgYGBAOIQwKHA4MFhIOEhIQFBAQGg4MChYUFBIOHgwK\
HA4KHAwMIQoIEhAQGA4MFBAOFhAMHAwKEhIOGg4KBhYWEBAQDhIQEhAOGgwKFBAMDhASDg\
4UFg4MFA4OEBAOGAwKEhAMHAoIFA4MEg4OJwQEFg4KBhQUCBISDg4QEA4OIQYGFgwKFAwM\
FA4KCBIQBhISDAwSFAwKEA4MDg4OFgoIDg4MDgwOEAwKDAwODg4KEgoIEAoKDgwKBhAODA\
wMCgwODAwKCgoODgoKCgwMFAgGCAwMDgoICgoKDggIBgwMFAYECgoICAgMBAwMBgoKCAgI\
BggKBAoKBggICAYIBAgIBgYICAYGBgYGBAYGBAYEBgQEBAQGAAAAAgICCgUCDgAAFQAAAQ\
EBAgMDBAQGBgYIBwgKCQoMCwwPDQ4RDhATEBEVEhMYExUaFRccFxkeGRshBwcHCwsLHR0d\
Hx8fJiYmEQAAAAAAAAgAABEAABoAACMAACwAADYAAD8A'


default_palettes = {
'ARC': ARC,
'BUYIT': BUYIT,
'DTENTION': DTENTION,
'EXECUTOR': EXECUTOR,
'FUELSTAT': FUELSTAT,
'GROMAS': GROMAS,
'IMPCITY': IMPCITY,
'JABSHIP': JABSHIP,
'NARSHADA': NARSHADA,
'RAMSHED': RAMSHED,
'ROBOTICS': ROBOTICS,
'SECBASE': SECBASE,
'SEWERS': SEWERS,
'TALAY': TALAY,
'TESTBASE': TESTBASE,
'WAIT': WAIT
}
