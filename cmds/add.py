from discord import Message
from itertools import zip_longest

from util import authors, layout, memory, parser
from util.consts import *

def exec(message: Message):
    name, string = parser.get_layout(message)

    if len(name) < 3:
        return 'Error: names must be at least 3 characters long'

    if not set(name).issubset(NAME_SET):
        disallowed = list(set(name).difference(NAME_SET))
        return f'Error: names cannot contain `{disallowed[0]}`'

    rows = string.split('\n')

    # calculate amount of leading whitespace for each row
    spaces = [] 
    for row in rows:
        size = len(row) - len(row.lstrip())
        spaces.append(size)

    # Determine board type with leading whitespace
    if spaces[0] < spaces[1] < spaces[2]:
        board = 'stagger'
    elif spaces[0] == spaces[1] < spaces[2]:
        board = 'angle'
    elif spaces[0] == spaces[1] == spaces[2]:
        board = 'ortho'
    else:
        return 'Error: board shape is undefined'

    if not is_rows_valid(string, board=board):
        return 'Error: improper number of rows in layout definition'

    rows = [x.strip() for x in rows] # remove leading/trailing whitespace

    gap = True # keep track of gap size
    columns = []
    for i, col in enumerate(zip_longest(*rows, fillvalue=' ')):

        if all(x == ' ' for x in col): # column gap detected
            gap = True
            continue
        
        if not gap: # no gap between letters
            return f'Error: missing gap before column `{col}`'

        columns.append(col)
        gap = False

    free = []
    keymap = {}
    for i, row in enumerate(zip(*columns)):
        for j, char in enumerate(row):

            if char in keymap: # duplicate
                return f'Error: `{char} is defined twice`'

            if char == ' ': # skip whitespace
                continue

            if board == 'angle' and i == 2:
                fmap = FMAP_ANGLE
            else:
                fmap = FMAP_STANDARD

            if i < 3:
                finger = fmap[min(j, len(fmap) - 1)]
            else:
                finger = 'TB' # thumb row

            data = {
                'row': i,
                'col': j,
                'finger': finger,
            }

            if char == FREE_CHAR: # free space
                free.append(data)
                continue

            keymap[char] = data

    # must include all letters except one
    if len(LETTERS) - len(list(x for x in keymap if x in LETTERS)) > len(free): 
        return 'Error: missing a required letter in layout definition'

    data = {
        'name': name,
        'user': message.author.id,
        'board': board,
        'keys': keymap,
        'free': free,
    }

    authors.update(message)

    if memory.add(data):
        return f'Success!\n' + layout.to_string(data, id=message.author.id)
    else:
        return f'Error: `{name}` already exists'


def use():
    return 'add [LAYOUT]'

def desc():
    return 'contribute a new layout'

def is_rows_valid(string: str, *, board: str) -> bool:
    rows = string.split('\n')

    if board in ['ortho']:
        max_rows = 4
    else:
        max_rows = 3

    return len(rows[1:]) <= max_rows