"""
Star Wars: Dark Forces WAX image functions.
"""
import struct
from formats import fme

WAX_VERSION = 0x00100100


class ActorAngle:
    def __init__(self):
        self.frame_offsets = []
        self.actor_frames = []


class ActorState:
    def __init__(self):
        self.world_width = 0
        self.world_height = 0
        self.frame_rate = 0
        self._num_frames = 0

        self.angle_offsets = []
        self.actor_angles = []

class Wax:
    def __init__(self):
        self.num_sequences = 0
        self.num_frames = 0
        self.num_cells = 0
        self._x_scale = 0
        self._y_scale = 0
        self._extra_light = 0

        self.state_offsets = []
        self.actor_states = []

def read(filename):
    wax = Wax()
    with open(filename, "rb") as file:
        if struct.unpack(">i", file.read(4))[0] != WAX_VERSION:
            raise Exception("WAX version is incorrect.")

        wax.num_sequences = struct.unpack("<i", file.read(4))[0]
        wax.num_frames = struct.unpack("<i", file.read(4))[0]
        wax.num_cells = struct.unpack("<i", file.read(4))[0]
        wax._x_scale = struct.unpack("<i", file.read(4))[0]
        wax._y_scale = struct.unpack("<i", file.read(4))[0]
        wax._extra_light = struct.unpack("<i", file.read(4))[0]
        # pad
        file.read(4)
        wax.state_offsets = struct.unpack("<32i", file.read(4 * 32))

        for state_offset in wax.state_offsets:
            if state_offset == 0:
                continue
            state = ActorState()
            file.seek(state_offset)
            state.world_width = struct.unpack("<i", file.read(4))[0]
            state.world_height = struct.unpack("<i", file.read(4))[0]
            state.frame_rate = struct.unpack("<i", file.read(4))[0]
            state.num_frames = struct.unpack("<i", file.read(4))[0]
            # pad
            file.read(4 * 3)
            state.angle_offsets = struct.unpack("<32i", file.read(4 * 32))
            wax.actor_states.append(state)

            # only keep unique viewing angles (offsets are repeated when the same angle has an identical view)
            # set also messes up the order of the offsets, so call sort()
            state.angle_offsets = list(set(state.angle_offsets))
            state.angle_offsets.sort()

        for state in wax.actor_states:
            for angle_offset in state.angle_offsets:
                if angle_offset == 0:
                    continue
                angle = ActorAngle()
                file.seek(angle_offset)
                # pad
                file.read(4 * 4)
                angle.frame_offsets = struct.unpack("<32i", file.read(4 * 32))
                state.actor_angles.append(angle)

        for state in wax.actor_states:
            for angle in state.actor_angles:
                for frame_offset in angle.frame_offsets:
                    if frame_offset == 0:
                        continue
                    else:
                        file.seek(frame_offset)
                        angle.actor_frames.append(fme.read_from_wax(file))

        return wax


def write(filename):
    pass


def to_png(wax, rgba_palette):
    pass


def to_pngs(wax, rgba_palette):
    pass


general_wax_states = {
0: "moving",
1: "attacking (primary)",
2: "dying (melee)",
3: "dying (bullet or explosion)",
4: "dead",
5: "idle",
6: "attack follow through (primary)",
7: "attacking (secondary)",
8: "attack follow through (secondary)",
9: "jumping",
10: "none",
11: "none",
12: "pain",
13: "special"
}

remote_wax_states = {
0: "moving",
1: "idle",
2: "dying",
3: "dying"
}

scenery_wax_states = {
0: "normal",
1: "destroyed"
}

barrel_wax_states = {
0: "normal",
1: "exploding"
}