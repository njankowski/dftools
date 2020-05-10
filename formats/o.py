class LEVObject:
    def __init__(self):
        self.obj_class = ''
        self.data = 0
        self.x = 0.00
        self.y = 0.00
        self.z = 0.00
        self.pch = 0.00
        self.yaw = 0.00
        self.rol = 0.00
        self.diff = 0
        self.sequence = {}


class LEVObjectFile:
    def __init__(self):
        self.version = ''
        self.levelname = ''
        self.pods = []
        self.sprs = []
        self.fmes = []
        self.sounds = []
        self.objects = []




class Tokenizer():
    def __init__(self, file):
        self.__file = file
        self.__current_line = None
        self.__current_tokens = None
        self.__active_comment = 0


    def __read_line(self):
        line = self.__file.readline()
        if line == '':
            raise Exception('No more lines.')
        return line.strip()


    def __clean_comments(self, line):
        while True:
            start_index = line.find('/*')
            end_index = line.find('*/')

            if start_index == -1 and end_index == -1:
                break
            elif start_index != -1 and end_index == -1:
                self.__active_comment += 1
                line = line[:start_index]
            elif start_index == -1 and end_index != -1:
                self.__active_comment -= 1
                line = line[end_index + 2:]
            else:
                line = line[:start_index] + line[end_index + 2:]

        return line


    def __next_line(self):
        line = self.__clean_comments(self.__read_line())
        while len(line) == 0 or self.__active_comment != 0:
            if self.__active_comment < 0:
                raise Exception('Bad comment nesting.')
            line = self.__clean_comments(self.__read_line())

        self.__current_line = line


    def next_token(self):
        if self.__current_line == None or len(self.__current_tokens) == 0:
            self.__next_line()
            self.__current_tokens = self.__current_line.split()

        return self.__current_tokens.pop(0)


    def next_tokens_in_line(self):
        if self.__current_line == None or len(self.__current_tokens) == 0:
            self.__next_line()
            self.__current_tokens = self.__current_line.split()

        tokens = self.__current_tokens[:]
        self.__current_tokens.clear()

        return tokens


    def peek_token(self, lookahead):
        if self.__current_line == None or len(self.__current_tokens) == 0:
            self.__next_line()
            self.__current_tokens = self.__current_line.split()

        if not 0 <= lookahead < len(self.__current_tokens):
            raise Exception('Bad lookahead value.')

        return self.__current_tokens[lookahead]


    def token_count(self):
        return len(self.__current_tokens)




def parse_object_sequence(tokenizer):
    try:
        if tokenizer.peek_token(0) != 'SEQ':
            return
    except:
        return

    sequence = {}

    sequence_token = tokenizer.next_token()
    if sequence_token != 'SEQ':
        raise Exception(f'Bad sequence keyword. Got "{sequence_token}"')

    while tokenizer.peek_token(0) != 'SEQEND':
        sequence_key = tokenizer.next_token()
        sequence_value = ''
        while ':' not in tokenizer.peek_token(0) and 'SEQEND' not in tokenizer.peek_token(0):
            sequence_value += ' ' + tokenizer.next_token()

        sequence_value = sequence_value.strip()
        if sequence_key in sequence:
            sequence[sequence_key].append(sequence_value)
        else:
            sequence[sequence_key] = [sequence_value]

    sequence_token = tokenizer.next_token()

    return sequence


def parse_object_class(tokenizer):
    class_keyword = tokenizer.next_token()
    if class_keyword != 'CLASS:':
        raise Exception(f'Bad CLASS keyword. Got "{class_keyword}"')

    class_token = tokenizer.next_token()

    return class_token


def parse_object_data(tokenizer):
    data_keyword = tokenizer.next_token()
    if data_keyword != 'DATA:':
        raise Exception(f'Bad DATA keyword. Got "{data_keyword}"')

    data_token = tokenizer.next_token()
    data = int(data_token)

    return data


def parse_object_x(tokenizer):
    x_keyword = tokenizer.next_token()
    if x_keyword != 'X:':
        raise Exception(f'Bad X keyword. Got "{x_keyword}"')

    x_token = tokenizer.next_token()
    x = float(x_token)

    return x


def parse_object_y(tokenizer):
    y_keyword = tokenizer.next_token()
    if y_keyword != 'Y:':
        raise Exception(f'Bad Y keyword. Got "{y_keyword}"')

    y_token = tokenizer.next_token()
    y = float(y_token)

    return y


def parse_object_z(tokenizer):
    z_keyword = tokenizer.next_token()
    if z_keyword != 'Z:':
        raise Exception(f'Bad Z keyword. Got "{z_keyword}"')

    z_token = tokenizer.next_token()
    z = float(z_token)

    return z


def parse_object_pch(tokenizer):
    pch_keyword = tokenizer.next_token()
    if pch_keyword != 'PCH:':
        raise Exception(f'Bad PCH keyword. Got "{pch_keyword}"')

    pch_token = tokenizer.next_token()
    pch = float(pch_token)

    return pch


def parse_object_yaw(tokenizer):
    yaw_keyword = tokenizer.next_token()
    if yaw_keyword != 'YAW:':
        raise Exception(f'Bad YAW keyword. Got "{yaw_keyword}"')

    yaw_token = tokenizer.next_token()
    yaw = float(yaw_token)

    return yaw


def parse_object_rol(tokenizer):
    rol_keyword = tokenizer.next_token()
    if rol_keyword != 'ROL:':
        raise Exception(f'Bad ROL keyword. Got "{rol_keyword}"')

    rol_token = tokenizer.next_token()
    rol = float(rol_token)

    return rol


def parse_object_diff(tokenizer):
    diff_keyword = tokenizer.next_token()
    if diff_keyword != 'DIFF:':
        raise Exception(f'Bad DIFF keyword. Got "{diff_keyword}"')

    diff_token = tokenizer.next_token()
    diff = int(diff_token)

    return diff


def parse_object(tokenizer):
    levobj = LEVObject()
    levobj.obj_class = parse_object_class(tokenizer)
    levobj.data = parse_object_data(tokenizer)
    levobj.x = parse_object_x(tokenizer)
    levobj.y = parse_object_y(tokenizer)
    levobj.z = parse_object_z(tokenizer)
    levobj.pch = parse_object_pch(tokenizer)
    levobj.yaw = parse_object_yaw(tokenizer)
    levobj.rol = parse_object_rol(tokenizer)
    levobj.diff = parse_object_diff(tokenizer)
    levobj.sequence = parse_object_sequence(tokenizer)

    return levobj


def parse_objects(tokenizer):
    objects_keyword = tokenizer.next_token()
    if objects_keyword != 'OBJECTS':
        raise Exception(f'Bad OBJECTS keyword. Got "{objects_keyword}"')

    objects_token = tokenizer.next_token()
    objects_count = int(objects_token)

    objects = []
    for i in range(objects_count):
        objects.append(parse_object(tokenizer))

    return objects


def parse_sound(tokenizer):
    sound_keyword = tokenizer.next_token()
    if sound_keyword != 'SOUND:':
        raise Exception(f'Bad SOUND keyword. Got "{sound_keyword}"')

    sound_keyword = tokenizer.next_token()

    return sound_keyword


def parse_sounds(tokenizer):
    sounds_keyword = tokenizer.next_token()
    if sounds_keyword != 'SOUNDS':
        raise Exception(f'Bad SOUNDS keyword. Got "{sounds_keyword}"')

    sounds_token = tokenizer.next_token()
    sounds_count = int(sounds_token)

    sounds = []
    for i in range(sounds_count):
        sounds.append(parse_sound(tokenizer))

    return sounds


def parse_fme(tokenizer):
    fme_keyword = tokenizer.next_token()
    if fme_keyword != 'FME:':
        raise Exception(f'Bad FME keyword. Got "{fme_keyword}"')

    fme_keyword = tokenizer.next_token()

    return fme_keyword


def parse_fmes(tokenizer):
    fmes_keyword = tokenizer.next_token()
    if fmes_keyword != 'FMES':
        raise Exception(f'Bad FMES keyword. Got "{fmes_keyword}"')

    fmes_token = tokenizer.next_token()
    fmes_count = int(fmes_token)

    fmes = []
    for i in range(fmes_count):
        fmes.append(parse_fme(tokenizer))

    return fmes


def parse_spr(tokenizer):
    spr_keyword = tokenizer.next_token()
    if spr_keyword != 'SPR:':
        raise Exception(f'Bad SPR keyword. Got "{spr_keyword}"')

    spr_keyword = tokenizer.next_token()

    return spr_keyword


def parse_sprs(tokenizer):
    sprs_keyword = tokenizer.next_token()
    if sprs_keyword != 'SPRS':
        raise Exception(f'Bad SPRS keyword. Got "{sprs_keyword}"')

    sprs_token = tokenizer.next_token()
    sprs_count = int(sprs_token)

    sprs = []
    for i in range(sprs_count):
        sprs.append(parse_spr(tokenizer))

    return sprs


def parse_pod(tokenizer):
    pod_keyword = tokenizer.next_token()
    if pod_keyword != 'POD:':
        raise Exception(f'Bad POD keyword. Got "{pod_keyword}"')

    pod_keyword = tokenizer.next_token()

    return pod_keyword


def parse_pods(tokenizer):
    pods_keyword = tokenizer.next_token()
    if pods_keyword != 'PODS':
        raise Exception(f'Bad PODS keyword. Got "{pods_keyword}"')

    pods_token = tokenizer.next_token()
    pods_count = int(pods_token)

    pods = []
    for i in range(pods_count):
        pods.append(parse_pod(tokenizer))

    return pods


def parse_levelname(tokenizer):
    levelname_keyword = tokenizer.next_token()
    if levelname_keyword != 'LEVELNAME':
        raise Exception(f'Bad level name keyword. Got "{levelname_keyword}"')

    levelname_token = tokenizer.next_token()

    return levelname_token


def parse_version(tokenizer):
    version_keyword = tokenizer.next_token()
    if version_keyword != 'O':
        raise Exception(f'Bad version keyword. Got "{version_keyword}"')

    version_token = tokenizer.next_token()
    if version_token != '1.1':
        raise Exception(f'Bad version. Got "{version_token}"')

    return version_token


def read(filename):
    with open(filename, 'rt', encoding='cp437') as file:
        tokenizer = Tokenizer(file)
        objects = LEVObjectFile()
        objects.version = parse_version(tokenizer)
        objects.levelname = parse_levelname(tokenizer)
        objects.pods = parse_pods(tokenizer)
        objects.sprs = parse_sprs(tokenizer)
        objects.fmes = parse_fmes(tokenizer)
        objects.sounds = parse_sounds(tokenizer)
        objects.objects = parse_objects(tokenizer)

        return objects




def write_objects(file, lev_objects):
    file.write(f'OBJECTS {len(lev_objects.objects)}\n')
    for lev_obj in lev_objects.objects:
        file.write('    CLASS: {:} DATA: {:} X: {:.2f} Y: {:.2f} Z: {:.2f} PCH: {:.2f} YAW: {:.2f} ROL: {:.2f} DIFF: {:}\n'.format(
            lev_obj.obj_class, lev_obj.data, lev_obj.x, lev_obj.y, lev_obj.z, lev_obj.pch, lev_obj.yaw, lev_obj.rol, lev_obj.diff))
        if lev_obj.sequence and len(lev_obj.sequence) > 0:
             file.write('        SEQ\n')
             for seq_key, seq_val in lev_obj.sequence.items():
                 for val in seq_val:
                    file.write(f'            {seq_key} {val}\n')
             file.write('        SEQEND\n')
    file.write('\n')


def write_sounds(file, lev_objects):
    file.write(f'SOUNDS {len(lev_objects.sounds)}\n')
    for sound in lev_objects.sounds:
        file.write(f'    SOUND: {sound}\n')
    file.write('\n')


def write_fmes(file, lev_objects):
    file.write(f'FMES {len(lev_objects.fmes)}\n')
    for fme in lev_objects.fmes:
        file.write(f'    FME: {fme}\n')
    file.write('\n')


def write_sprs(file, lev_objects):
    file.write(f'SPRS {len(lev_objects.sprs)}\n')
    for spr in lev_objects.sprs:
        file.write(f'    SPR: {spr}\n')
    file.write('\n')


def write_pods(file, lev_objects):
    file.write(f'PODS {len(lev_objects.pods)}\n')
    for pod in lev_objects.pods:
        file.write(f'    POD: {pod}\n')
    file.write('\n')


def write_levelname(file, lev_objects):
    file.write(f'LEVELNAME {lev_objects.levelname}\n')
    file.write('\n')


def write_version(file, lev_objects):
    file.write(f'O 1.1\n')
    file.write('\n')


def write(filename, lev_objects):
    with open(filename, 'wt', encoding='cp437') as file:
        write_version(file, lev_objects)
        write_levelname(file, lev_objects)
        write_pods(file, lev_objects)
        write_sprs(file, lev_objects)
        write_fmes(file, lev_objects)
        write_sounds(file, lev_objects)
        write_objects(file, lev_objects)
