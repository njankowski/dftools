class Vertex:
    def __init__(self):
        self.x = 0
        self.z = 0


class Wall:
    def __init__(self):
        self.left_vertex = 0
        self.right_vertex = 0
        self.middle_texture = (0, 0.0, 0.0)
        self.top_texture = (0, 0.0, 0.0)
        self.bottom_texture = (0, 0.0, 0.0)
        self.sign_texture = (0, 0.0, 0.0)
        self.adjoin = 0
        self.mirror = 0
        self.walk = 0
        self.flags = (0, 0, 0)
        self.light = 0


class Sector:
    def __init__(self):
        self.id = 0,
        self.name = ''
        self.ambient = 0
        self.floor_texture = (0, 0.0, 0.0)
        self.floor_altitude = 0.0,
        self.ceiling_texture = (0, 0.0, 0.0)
        self.ceiling_altitude = 0.0
        self.second_altitude = 0.0
        self.flags = (0, 0, 0)
        self.layer = 0
        self.vertices = []
        self.walls = []


class Level:
    def __init__(self):
        self.version = ''
        self.levelname = ''
        self.palette = ''
        self.music = ''
        self.parallax = (0.0, 0.0)
        self.textures = []
        self.sectors = []


class Tokenizer():
    def __init__(self, file):
        self.__file = file
        self.__current_line = None
        self.__current_tokens = None


    def __next_line(self):
        line = self.__file.readline()
        if line == '':
            raise Exception('No more lines.')
        line = line.strip().partition('#')[0]

        while len(line) == 0:
            line = self.__file.readline()
            if line == '':
                raise Exception('No more lines.')
            line = line.strip().partition('#')[0]

        self.__current_line = line


    def next_token(self):
        if self.__current_line == None or len(self.__current_tokens) == 0:
            self.__next_line()
            self.__current_tokens = self.__current_line.split()

        return self.__current_tokens.pop(0)


    def peek_token(self, lookahead):
        if self.__current_line == None or len(self.__current_tokens) == 0:
            self.__next_line()
            self.__current_tokens = self.__current_line.split()

        if not 0 <= lookahead < len(self.__current_tokens):
            raise Exception('Bad lookahead value.')

        return self.__current_tokens[lookahead]


    def token_count(self):
        return len(self.__current_tokens)


def parse_wall_light(tokenizer):
    light_keyword = tokenizer.next_token()
    if light_keyword != 'LIGHT:':
        raise Exception(f'Bad light keyword. Got "{light_keyword}"')

    light_token = tokenizer.next_token()
    light = int(light_token)

    return light


def parse_wall_flags(tokenizer):
    flags_keyword = tokenizer.next_token()
    if flags_keyword != 'FLAGS:':
        raise Exception(f'Bad flags keyword. Got "{flags_keyword}"')

    flag_one_token = tokenizer.next_token()
    flag_one = int(flag_one_token)

    flag_two_token = tokenizer.next_token()
    flag_two = int(flag_two_token)

    flag_three_token = tokenizer.next_token()
    flag_three = int(flag_three_token)

    return (flag_one, flag_two, flag_three)


def parse_wall_walk(tokenizer):
    walk_keyword = tokenizer.next_token()
    if walk_keyword != 'WALK:':
        raise Exception(f'Bad walk keyword. Got "{walk_keyword}"')

    walk_token = tokenizer.next_token()
    walk = int(walk_token)

    return walk


def parse_wall_mirror(tokenizer):
    mirror_keyword = tokenizer.next_token()
    if mirror_keyword != 'MIRROR:':
        raise Exception(f'Bad mirror keyword. Got "{mirror_keyword}"')

    mirror_token = tokenizer.next_token()
    mirror = int(mirror_token)

    return mirror


def parse_wall_adjoin(tokenizer):
    adjoin_keyword = tokenizer.next_token()
    if adjoin_keyword != 'ADJOIN:':
        raise Exception(f'Bad adjoin keyword. Got "{adjoin_keyword}"')

    adjoin_token = tokenizer.next_token()
    adjoin = int(adjoin_token)

    return adjoin


def parse_wall_sign_texture(tokenizer):
    sign_texture_keyword = tokenizer.next_token()
    if sign_texture_keyword != 'SIGN:':
        raise Exception(f'Bad sign texture keyword. Got "{sign_texture_keyword}"')

    sign_texture_index_token = tokenizer.next_token()
    sign_texture_index = int(sign_texture_index_token)

    sign_texture_x_offset_token = tokenizer.next_token()
    sign_texture_x_offset = float(sign_texture_x_offset_token)

    sign_texture_y_offset_token = tokenizer.next_token()
    sign_texture_y_offset = float(sign_texture_y_offset_token)

    return (sign_texture_index, sign_texture_x_offset, sign_texture_y_offset)


def parse_wall_bottom_texture(tokenizer):
    bot_texture_keyword = tokenizer.next_token()
    if bot_texture_keyword != 'BOT:':
        raise Exception(f'Bad bottom texture keyword. Got "{bot_texture_keyword}"')

    bot_texture_index_token = tokenizer.next_token()
    bot_texture_index = int(bot_texture_index_token)

    bot_texture_x_offset_token = tokenizer.next_token()
    bot_texture_x_offset = float(bot_texture_x_offset_token)

    bot_texture_y_offset_token = tokenizer.next_token()
    bot_texture_y_offset = float(bot_texture_y_offset_token)

    # Consume unused token.
    tokenizer.next_token()

    return (bot_texture_index, bot_texture_x_offset, bot_texture_y_offset)


def parse_wall_top_texture(tokenizer):
    top_texture_keyword = tokenizer.next_token()
    if top_texture_keyword != 'TOP:':
        raise Exception(f'Bad top texture keyword. Got "{top_texture_keyword}"')

    top_texture_index_token = tokenizer.next_token()
    top_texture_index = int(top_texture_index_token)

    top_texture_x_offset_token = tokenizer.next_token()
    top_texture_x_offset = float(top_texture_x_offset_token)

    top_texture_y_offset_token = tokenizer.next_token()
    top_texture_y_offset = float(top_texture_y_offset_token)

    # Consume unused token.
    tokenizer.next_token()

    return (top_texture_index, top_texture_x_offset, top_texture_y_offset)


def parse_wall_middle_texture(tokenizer):
    mid_texture_keyword = tokenizer.next_token()
    if mid_texture_keyword != 'MID:':
        raise Exception(f'Bad middle texture keyword. Got "{mid_texture_keyword}"')

    mid_texture_index_token = tokenizer.next_token()
    mid_texture_index = int(mid_texture_index_token)

    mid_texture_x_offset_token = tokenizer.next_token()
    mid_texture_x_offset = float(mid_texture_x_offset_token)

    mid_texture_y_offset_token = tokenizer.next_token()
    mid_texture_y_offset = float(mid_texture_y_offset_token)

    # Consume unused token.
    tokenizer.next_token()

    return (mid_texture_index, mid_texture_x_offset, mid_texture_y_offset)


def parse_wall_right_vertex(tokenizer):
    right_keyword = tokenizer.next_token()
    if right_keyword != 'RIGHT:':
        raise Exception(f'Bad right keyword. Got "{right_keyword}"')

    right_token = tokenizer.next_token()
    wall_right = int(right_token)

    return wall_right


def parse_wall_left_vertex(tokenizer):
    left_keyword = tokenizer.next_token()
    if left_keyword != 'LEFT:':
        raise Exception(f'Bad left keyword. Got "{left_keyword}"')

    left_token = tokenizer.next_token()
    wall_left = int(left_token)

    return wall_left


def parse_wall(tokenizer):
    wall_keyword = tokenizer.next_token()
    if wall_keyword != 'WALL':
        raise Exception(f'Bad wall keyword. Got "{wall_keyword}"')

    wall = Wall()

    wall.left_vertex = parse_wall_left_vertex(tokenizer)
    wall.right_vertex = parse_wall_right_vertex(tokenizer)
    wall.middle_texture = parse_wall_middle_texture(tokenizer)
    wall.top_texture = parse_wall_top_texture(tokenizer)
    wall.bottom_texture = parse_wall_bottom_texture(tokenizer)
    wall.sign_texture = parse_wall_sign_texture(tokenizer)
    wall.adjoin = parse_wall_adjoin(tokenizer)
    wall.mirror = parse_wall_mirror(tokenizer)
    wall.walk = parse_wall_walk(tokenizer)
    wall.flags = parse_wall_flags(tokenizer)
    wall.light = parse_wall_light(tokenizer)

    return wall


def parse_walls(tokenizer):
    walls_keyword = tokenizer.next_token()
    if walls_keyword != 'WALLS':
        raise Exception(f'Bad walls keyword. Got "{walls_keyword}"')

    walls_token = tokenizer.next_token()
    walls_count = int(walls_token)

    walls = []
    for i in range(walls_count):
        walls.append(parse_wall(tokenizer))

    return walls


def parse_vertex_z(tokenizer):
    z_keyword = tokenizer.next_token()
    if z_keyword != 'Z:':
        raise Exception(f'Bad Z keyword. Got "{z_keyword}"')

    z_token = tokenizer.next_token()
    z = float(z_token)

    return z


def parse_vertex_x(tokenizer):
    x_keyword = tokenizer.next_token()
    if x_keyword != 'X:':
        raise Exception(f'Bad X keyword. Got "{x_keyword}"')

    x_token = tokenizer.next_token()
    x = float(x_token)

    return x


def parse_vertex(tokenizer):
    vertex = Vertex()

    vertex.x = parse_vertex_x(tokenizer)
    vertex.z = parse_vertex_z(tokenizer)

    return vertex


def parse_vertices(tokenizer):
    vertices_keyword = tokenizer.next_token()
    if vertices_keyword != 'VERTICES':
        raise Exception(f'Bad vertices keyword. Got "{vertices_keyword}"')

    vertices_token = tokenizer.next_token()
    vertices_count = int(vertices_token)

    vertices = []
    for i in range(vertices_count):
        vertices.append(parse_vertex(tokenizer))

    return vertices


def parse_sector_layer(tokenizer):
    layer_keyword = tokenizer.next_token()
    if layer_keyword != 'LAYER':
        raise Exception(f'Bad layer keyword. Got "{layer_keyword}"')

    layer_token = tokenizer.next_token()
    layer = int(layer_token)

    return layer


def parse_sector_flags(tokenizer):
    flags_keyword = tokenizer.next_token()
    if flags_keyword != 'FLAGS':
        raise Exception(f'Bad flags keyword. Got "{flags_keyword}"')

    flag_one_token = tokenizer.next_token()
    flag_one = int(flag_one_token)

    flag_two_token = tokenizer.next_token()
    flag_two = int(flag_two_token)

    flag_three_token = tokenizer.next_token()
    flag_three = int(flag_three_token)

    return (flag_one, flag_two, flag_three)


def parse_sector_second_altitude(tokenizer):
    # Avoid checking two tokens by concatenating the split keyword.
    second_altitude_keyword = tokenizer.next_token() + ' ' + tokenizer.next_token()
    if second_altitude_keyword != 'SECOND ALTITUDE':
        raise Exception(f'Bad second altitude keyword. Got "{second_altitude_keyword}"')

    second_altitude_token = tokenizer.next_token()
    second_altitude = float(second_altitude_token)

    return second_altitude


def parse_sector_ceiling_altitude(tokenizer):
    # Avoid checking two tokens by concatenating the split keyword.
    ceiling_altitude_keyword = tokenizer.next_token() + ' ' + tokenizer.next_token()
    if ceiling_altitude_keyword != 'CEILING ALTITUDE':
        raise Exception(f'Bad ceiling altitude keyword. Got "{ceiling_altitude_keyword}"')

    ceiling_altitude_token = tokenizer.next_token()
    ceiling_altitude = float(ceiling_altitude_token)

    return ceiling_altitude


def parse_sector_ceiling_texture(tokenizer):
    # Avoid checking two tokens by concatenating the split keyword.
    ceiling_texture_keyword = tokenizer.next_token() + ' ' + tokenizer.next_token()
    if ceiling_texture_keyword != 'CEILING TEXTURE':
        raise Exception(f'Bad ceiling texture keyword. Got "{ceiling_texture_keyword}"')

    ceiling_texture_index_token = tokenizer.next_token()
    ceiling_texture_index = int(ceiling_texture_index_token)

    ceiling_texture_x_offset_token = tokenizer.next_token()
    ceiling_texture_x_offset = float(ceiling_texture_x_offset_token)

    ceiling_texture_y_offset_token = tokenizer.next_token()
    ceiling_texture_y_offset = float(ceiling_texture_y_offset_token)

    # Consume unused token.
    tokenizer.next_token()

    return (ceiling_texture_index, ceiling_texture_x_offset, ceiling_texture_y_offset)


def parse_sector_floor_altitude(tokenizer):
    # Avoid checking two tokens by concatenating the split keyword.
    floor_altitude_keyword = tokenizer.next_token() + ' ' + tokenizer.next_token()
    if floor_altitude_keyword != 'FLOOR ALTITUDE':
        raise Exception(f'Bad floor altitude keyword. Got "{floor_altitude_keyword}"')

    floor_altitude_token = tokenizer.next_token()
    floor_altitude = float(floor_altitude_token)

    return floor_altitude


def parse_sector_floor_texture(tokenizer):
    # Avoid checking two tokens by concatenating the split keyword.
    floor_texture_keyword = tokenizer.next_token() + ' ' + tokenizer.next_token()
    if floor_texture_keyword != 'FLOOR TEXTURE':
        raise Exception(f'Bad floor texture keyword. Got "{floor_texture_keyword}"')

    floor_texture_index_token = tokenizer.next_token()
    floor_texture_index = int(floor_texture_index_token)

    floor_texture_x_offset_token = tokenizer.next_token()
    floor_texture_x_offset = float(floor_texture_x_offset_token)

    floor_texture_y_offset_token = tokenizer.next_token()
    floor_texture_y_offset = float(floor_texture_y_offset_token)

    # Consume unused token.
    tokenizer.next_token()

    return (floor_texture_index, floor_texture_x_offset, floor_texture_y_offset)


def parse_sector_ambient(tokenizer):
    ambient_keyword = tokenizer.next_token()
    if ambient_keyword != 'AMBIENT':
        raise Exception(f'Bad ambient keyword. Got "{ambient_keyword}"')

    ambient_token = tokenizer.next_token()
    sector_ambient = int(ambient_token)

    return sector_ambient


def parse_sector_name(tokenizer):
    name_keyword = tokenizer.next_token()
    if name_keyword != 'NAME':
        raise Exception(f'Bad name keyword. Got "{name_keyword}"')

    sector_name = ''
    if tokenizer.token_count() != 0:
        name_token = tokenizer.next_token()
        sector_name = name_token

    return sector_name


def parse_sector_id(tokenizer):
    sector_keyword = tokenizer.next_token()
    if sector_keyword != 'SECTOR':
        raise Exception(f'Bad sector keyword. Got "{sector_keyword}"')

    sector_token = tokenizer.next_token()
    sector_id = int(sector_token)

    return sector_id


def parse_sector(tokenizer):
    sector = Sector()

    sector.id = parse_sector_id(tokenizer)
    sector.name = parse_sector_name(tokenizer)
    sector.ambient = parse_sector_ambient(tokenizer)
    sector.floor_texture = parse_sector_floor_texture(tokenizer)
    sector.floor_altitude = parse_sector_floor_altitude(tokenizer)
    sector.ceiling_texture = parse_sector_ceiling_texture(tokenizer)
    sector.ceiling_altitude = parse_sector_ceiling_altitude(tokenizer)
    sector.second_altitude = parse_sector_second_altitude(tokenizer)
    sector.flags = parse_sector_flags(tokenizer)
    sector.layer = parse_sector_layer(tokenizer)
    sector.vertices = parse_vertices(tokenizer)
    sector.walls = parse_walls(tokenizer)

    return sector


def parse_sectors(tokenizer):
    sectors_keyword = tokenizer.next_token()
    if sectors_keyword != 'NUMSECTORS':
        raise Exception(f'Bad sectors keyword. Got "{sectors_keyword}"')

    sectors_token = tokenizer.next_token()
    sectors_count = int(sectors_token)

    sectors = []
    for i in range(sectors_count):
        sectors.append(parse_sector(tokenizer))

    return sectors


def parse_texture(tokenizer):
    texture_keyword = tokenizer.next_token()
    if texture_keyword != 'TEXTURE:':
        raise Exception(f'Bad texture keyword. Got "{texture_keyword}"')

    texture_token = tokenizer.next_token()

    return texture_token


def parse_textures(tokenizer):
    textures_keyword = tokenizer.next_token()
    if textures_keyword != 'TEXTURES':
        raise Exception(f'Bad textures keyword. Got "{textures_keyword}"')

    textures_token = tokenizer.next_token()
    textures_count = int(textures_token)

    textures = []
    for i in range(textures_count):
        textures.append(parse_texture(tokenizer))

    return textures


def parse_parallax(tokenizer):
    parallax_keyword = tokenizer.next_token()
    if parallax_keyword != 'PARALLAX':
        raise Exception(f'Bad parallax keyword. Got "{parallax_keyword}"')

    parallax_x_token = tokenizer.next_token()
    parallax_y_token = tokenizer.next_token()

    return (float(parallax_x_token), float(parallax_y_token))


def parse_music(tokenizer):
    if tokenizer.peek_token(0) != 'MUSIC':
        return ''

    music_keyword = tokenizer.next_token()
    if music_keyword != 'MUSIC':
        raise Exception(f'Bad music keyword. Got "{music_keyword}"')

    music_token = tokenizer.next_token()

    return music_token


def parse_palette(tokenizer):
    palette_keyword = tokenizer.next_token()
    if palette_keyword != 'PALETTE':
        raise Exception(f'Bad palette keyword. Got "{palette_keyword}"')

    palette_token = tokenizer.next_token()

    return palette_token


def parse_levelname(tokenizer):
    levelname_keyword = tokenizer.next_token()
    if levelname_keyword != 'LEVELNAME':
        raise Exception(f'Bad level name keyword. Got "{levelname_keyword}"')

    levelname_token = tokenizer.next_token()

    return levelname_token


def parse_version(tokenizer):
    version_keyword = tokenizer.next_token()
    if version_keyword != 'LEV':
        raise Exception(f'Bad version keyword. Got "{version_keyword}"')

    version_token = tokenizer.next_token()
    if version_token != '2.1':
        raise Exception(f'Bad version. Got "{version_token}"')

    return version_token


def read(filename):
    with open(filename, 'rt', encoding='cp437') as file:
        tokenizer = Tokenizer(file)
        level = Level()
        level.version = parse_version(tokenizer)
        level.levelname = parse_levelname(tokenizer)
        level.palette = parse_palette(tokenizer)
        level.music = parse_music(tokenizer)
        level.parallax = parse_parallax(tokenizer)
        level.textures = parse_textures(tokenizer)
        level.sectors = parse_sectors(tokenizer)

        return level


def write_sector(file, sector):
    file.write(f'  SECTOR {sector.id}\n')
    file.write(f'    NAME {sector.name}\n')
    file.write(f'    AMBIENT {sector.ambient}\n')
    file.write('    FLOOR TEXTURE {:} {:.2f} {:.2f} {:}\n'.format(*sector.floor_texture, 0))
    file.write('    FLOOR ALTITUDE {:.2f}\n'.format(sector.floor_altitude))
    file.write('    CEILING TEXTURE {:} {:.2f} {:.2f} {:}\n'.format(*sector.ceiling_texture, 0))
    file.write('    CEILING ALTITUDE {:.2f}\n'.format(sector.ceiling_altitude))
    file.write('    SECOND ALTITUDE {:.2f}\n'.format(sector.second_altitude))
    file.write('    FLAGS {:} {:} {:}\n'.format(*sector.flags))
    file.write('    LAYER {:}\n'.format(sector.layer))

    #file.write('    VERTICES {:05}\n'.format(len(sector.vertices)))
    file.write('    VERTICES {:}\n'.format(len(sector.vertices)))
    for vertex in sector.vertices:
        file.write('      X: {:.2f} Z: {:.2f}\n'.format(vertex.x, vertex.z))

    file.write(f'    WALLS {len(sector.walls)}\n')
    for wall in sector.walls:
        file.write('      WALL LEFT: {:} RIGHT: {:} MID: {:} {:.2f} {:.2f} {:} TOP: {:} {:.2f} {:.2f} {:} BOT: {:} {:.2f} {:.2f} {:} SIGN: {:} {:.2f} {:.2f} ADJOIN: {:}  MIRROR: {:} WALK: {:} FLAGS: {:} {:} {:} LIGHT: {:}\n'.format(
            wall.left_vertex, wall.right_vertex, *wall.middle_texture, 0, *wall.top_texture, 0, *wall.bottom_texture, 0, *wall.sign_texture, wall.adjoin, wall.mirror, wall.walk, *wall.flags, wall.light))


def write_sectors(file, level):
    file.write(f'NUMSECTORS {len(level.sectors)}\n')
    for sector in level.sectors:
        write_sector(file, sector)
        file.write('\n')


def write_textures(file, level):
    file.write(f'TEXTURES {len(level.textures)}\n')
    for texture in level.textures:
        file.write(f'  TEXTURE: {texture}\n')
    file.write('\n')


def write_parallax(file, level):
    #file.write('PARALLAX {:.4f} {:.4f}\n'.format(*level.parallax))
    file.write('PARALLAX {:.2f} {:.2f}\n'.format(*level.parallax))
    file.write('\n')


def write_music(file, level):
    file.write(f'MUSIC {level.music}\n')


def write_palette(file, level):
    file.write(f'PALETTE {level.palette}\n')


def write_levelname(file, level):
    file.write(f'LEVELNAME {level.levelname}\n')


def write_version(file, level):
    file.write(f'LEV 2.1\n')


def write(filename, level):
    with open(filename, 'wt', encoding='cp437') as file:
        write_version(file, level)
        write_levelname(file, level)
        write_palette(file, level)
        write_music(file, level)
        write_parallax(file, level)
        write_textures(file, level)
        write_sectors(file, level)
