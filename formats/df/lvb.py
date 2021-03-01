import struct
from lev import Level, Sector, Wall, Vertex


def read_wall_light(file):
    pass


def read_wall_flags(file):
    pass


def read_wall_walk(file):
    pass


def read_wall_mirror(file):
    pass


def read_wall_adjoin(file):
    pass


def read_wall_sign_texture(file):
    pass


def read_wall_bottom_texture(file):
    pass


def read_wall_top_texture(file):
    pass


def read_wall_middle_texture(file):
    pass


def read_wall_right_vertex(file):
    pass


def read_wall_left_vertex(file):
    pass


def read_wall(file):
    pass


def read_walls(file):
    pass


def read_vertex_z(file):
    pass


def read_vertex_x(file):
    pass


def read_vertex(file):
    pass


def read_vertices(file):
    pass


def read_sector_layer(file):
    pass


def read_sector_flags(file):
    pass


def read_sector_second_altitude(file):
    pass


def read_sector_ceiling_altitude(file):
    pass


def read_sector_ceiling_texture(file):
    pass


def read_sector_floor_altitude(file):
    pass


def read_sector_floor_texture(file):
    pass


def read_sector_ambient(file):
    pass


def read_sector_name(file):
    pass


def read_sector_id(file):
    pass


def read_sector(file):
    pass


def read_sectors(file):
    pass


def read_texture(file):
    pass


def read_textures(file):
    pass


def read_parallax(file):
    pass


def read_music(file):
    pass


def read_palette(file):
    pass


def read_levelname(file):
    pass


def read_version(file):
    if file.read(4) != b'VER':
        raise Exception('Bad version identifier.')

    major_version = struct.unpack('B', file.read(1))[0]
    minor_version = struct.unpack('B', file.read(1))[0]

    # Consume unknown byte field.
    file.read(1)

    return (major_version, minor_version)


def read_header(file):
    if file.read(4) != b'LVB':
        raise Exception('Bad identifier.')

    # Consume unknown byte field.
    file.read(1)

    lvb_size = struct.unpack('<I', file.read(4))[0]
    return lvb_size



def read(filename):
    with open(filename, 'rb') as file:
        level = Level()

        lvb_size = read_header(file)

        level.version = read_version(file)
        level.levelname = read_levelname(file)
        level.palette = read_palette(file)
        level.music = read_music(file)
        level.parallax = read_parallax(file)
        level.textures = read_textures(file)
        level.sectors = read_sectors(file)

        end_pos = file.tell()
        if end_pos - 8 != lvb_size:
            raise Exception('Total size in header does not match expected length.')

        return level


def write(filename, level):
    with open(filename, 'wb') as file:
        pass
