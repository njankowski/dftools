class VUEFile:
    def __init__(self):
        self.alternate_format = None
        self.version = None
        self.frames = []




class Tokenizer():
    def __init__(self, file):
        self.__file = file
        self.__current_line = None
        self.__current_tokens = None


    def __next_line(self):
        line = self.__file.readline()
        if line == '':
            raise Exception('No more lines.')
        line = line.strip()

        while len(line) == 0:
            line = self.__file.readline()
            if line == '':
                raise Exception('No more lines.')
            line = line.strip()

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




def parse_frames_alternate(tokenizer):
    frames = []
    while True:
        try:
            frame = {}
            frame_keyword = tokenizer.next_token()
            if frame_keyword != 'vue':
                raise Exception(f'Bad alternate frame keyword. Got "{frame_keyword}"')

            frame_token = tokenizer.next_token()
            frame_number = int(frame_token)

            frame['vue'] = frame_number

            while tokenizer.peek_token(0) != 'vue':
                command_tokens = tokenizer.next_tokens_in_line()
                command = command_tokens[0]
                command_parameters = command_tokens[1:]

                if command in frame:
                    frame[command].append(' '.join(command_parameters))
                else:
                    frame[command] = [' '.join(command_parameters)]

            frames.append(frame)
        except:
            frames.append(frame)
            break

    return frames


def parse_frames(tokenizer):
    frames = []
    while True:
        try:
            frame = {}
            frame_keyword = tokenizer.next_token()
            if frame_keyword != 'frame':
                raise Exception(f'Bad frame keyword. Got "{frame_keyword}"')

            frame_token = tokenizer.next_token()
            frame_number = int(frame_token)

            frame['frame'] = frame_number

            while tokenizer.peek_token(0) != 'frame':
                command_tokens = tokenizer.next_tokens_in_line()
                command = command_tokens[0]
                command_parameters = command_tokens[1:]

                if command in frame:
                    frame[command].append(' '.join(command_parameters))
                else:
                    frame[command] = [' '.join(command_parameters)]

            frames.append(frame)
        except:
            frames.append(frame)
            break

    return frames


def check_alternate_format(tokenizer):
    alternate_keyword = tokenizer.peek_token(0)
    if alternate_keyword == 'vue':
        return True
    else:
        return False


def parse_version(tokenizer):
    version_keyword = tokenizer.peek_token(0)
    if version_keyword != 'VERSION':
        return None

    version_keyword = tokenizer.next_token()
    if version_keyword != 'VERSION':
        raise Exception(f'Bad version keyword. Got "{version_keyword}"')

    version_token = tokenizer.next_token()
    if version_token != '201':
        raise Exception(f'Bad version. Got "{version_token}"')

    return version_token


def read(filename):
    with open(filename, 'rt', encoding='cp437') as file:
        tokenizer = Tokenizer(file)
        vue_file = VUEFile()
        vue_file.version = parse_version(tokenizer)

        if vue_file.version is None:
            vue_file.alternate_format = check_alternate_format(tokenizer)

        if not vue_file.alternate_format:
            vue_file.frames = parse_frames(tokenizer)
        else:
            vue_file.frames = parse_frames_alternate(tokenizer)

        return vue_file

def write_frames_alternate(file, vue_file):
    for frame in vue_file.frames:
        for command_key, command_val in frame.items():
            if command_key == 'vue':
                file.write(f'{command_key} {command_val}\n')
            else:
                for subcommand in command_val:
                    file.write(f'{command_key} {subcommand}\n')
        file.write('\n')


def write_frames(file, vue_file):
    for frame in vue_file.frames:
        for command_key, command_val in frame.items():
            if command_key == 'frame':
                file.write(f'{command_key} {command_val}\n')
            else:
                for subcommand in command_val:
                    file.write(f'{command_key} {subcommand}\n')
        file.write('\n')


def write_version(file, vue_file):
    file.write(f'VERSION 201\n')
    file.write('\n')


def write(filename, vue_file):
    with open(filename, 'wt', encoding='cp437') as file:
        if vue_file.version:
            write_version(file, vue_file)

        if not vue_file.alternate_format:
            write_frames(file, vue_file)
        else:
            write_frames_alternate(file, vue_file)
