class INFAttribute:
    def __init__(self):
        self.name = None
        self.value = None


class LEVInfItem:
    def __init__(self):
        # level, sector, line
        self.item_type = None
        self.item_name = None
        self.wall_number = None
        self.sequence = None


class LEVInfFile:
    def __init__(self):
        self.version = ''
        self.levelname = ''
        self.items = []




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


def parse_sequence(tokenizer):
    # Sequences are order dependent.
    sequence = []

    sequence_token = tokenizer.next_token().lower()
    if sequence_token != 'seq':
        raise Exception(f'Bad sequence keyword. Got "{sequence_token}"')

    while tokenizer.peek_token(0).lower() != 'seqend':
        sequence_key = tokenizer.next_token()
        sequence_value = ''
        while ':' not in tokenizer.peek_token(0) and 'seqend' not in tokenizer.peek_token(0).lower():
            sequence_value += ' ' + tokenizer.next_token()

        attribute = INFAttribute()
        attribute.name = sequence_key
        attribute.value = sequence_value

        sequence.append(attribute)

    sequence_token = tokenizer.next_token()

    return sequence


def parse_wall_number(tokenizer):
    if tokenizer.peek_token(0).lower() != 'num:':
        return

    num_keyword = tokenizer.next_token().lower()
    if num_keyword != 'num:':
        raise Exception(f'Bad number keyword. Got "{num_keyword}"')

    num_token = tokenizer.next_token()
    num = int(num_token)

    return num


def parse_item_name(tokenizer):
    name_keyword = tokenizer.next_token().lower()
    if name_keyword != 'name:':
        raise Exception(f'Bad name keyword. Got "{name_keyword}"')

    name_token = tokenizer.next_token()

    return name_token


def parse_item_type(tokenizer):
    item_keyword = tokenizer.next_token().lower()
    if item_keyword != 'item:':
        raise Exception(f'Bad item keyword. Got "{item_keyword}"')

    item_token = tokenizer.next_token()

    return item_token


def parse_item(tokenizer):
    item = LEVInfItem()
    item.item_type = parse_item_type(tokenizer)
    item.item_name = parse_item_name(tokenizer)
    item.wall_number = parse_wall_number(tokenizer)
    item.sequence = parse_sequence(tokenizer)

    return item


def parse_items(tokenizer):
    # case insensitive
    items_keyword = tokenizer.next_token().lower()
    if items_keyword != 'items':
        raise Exception(f'Bad items keyword. Got "{items_keyword}"')

    # Item count is not always accurate and should be ignored.
    items_token = tokenizer.next_token()
    items_count = int(items_token)

    # Parse as many items as possible.
    items = []
    while True:
        try:
            items.append(parse_item(tokenizer))
        except:
            break

    return items


def parse_levelname(tokenizer):
    # case insensitive
    levelname_keyword = tokenizer.next_token().lower()
    if levelname_keyword != 'levelname':
        raise Exception(f'Bad level name keyword. Got "{levelname_keyword}"')

    levelname_token = tokenizer.next_token()

    return levelname_token


def parse_version(tokenizer):
    # case insensitive
    version_keyword = tokenizer.next_token().lower()
    if version_keyword != 'inf':
        raise Exception(f'Bad version keyword. Got "{version_keyword}"')

    version_token = tokenizer.next_token()
    if version_token != '1.0':
        raise Exception(f'Bad version. Got "{version_token}"')

    return version_token


def read(filename):
    with open(filename, 'rt', encoding='cp437') as file:
        tokenizer = Tokenizer(file)
        inf_file = LEVInfFile()
        inf_file.version = parse_version(tokenizer)
        inf_file.levelname = parse_levelname(tokenizer)
        inf_file.items = parse_items(tokenizer)

        return inf_file


def write_items(file, inf_objects):
    file.write(f'items {len(inf_objects.items)}\n')
    for item in inf_objects.items:
        file.write(f'  item: {item.item_type} name: {item.item_name}')
        if item.wall_number != None:
            file.write(f' num: {item.wall_number}')
        file.write('\n')
        file.write('    seq\n')
        for attribute in item.sequence:
            file.write(f'      {attribute.name} {attribute.value}\n')
        file.write('    seqend\n')


def write_levelname(file, inf_objects):
    file.write(f'levelname {inf_objects.levelname}\n')
    file.write('\n')


def write_version(file, inf_objects):
    file.write(f'inf 1.0\n')
    file.write('\n')


def write(filename, inf_objects):
    with open(filename, 'wt', encoding='cp437') as file:
        write_version(file, inf_objects)
        write_levelname(file, inf_objects)
        write_items(file, inf_objects)
