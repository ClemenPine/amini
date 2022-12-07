import json
import glob
from discord import Message

from util import authors, parser

def exec(message: Message):
    arg = parser.get_arg(message)
    
    if arg:
        id = authors.get_id(arg)
        name = arg
    else:
        id = message.author.id
        name = message.author.name

    if not id:
        return f'Error: user `{arg}` does not exist'

    lines = [f'{name}\'s layouts:']
    lines.append('```')

    layouts = []
    for file in glob.glob('layouts/*.json'):
        with open(file, 'r') as f:
            data = json.load(f)

        if data['user'] == id:
            layouts.append(data['name'])

    lines += list(sorted(layouts))
    lines.append('```')

    return '\n'.join(lines)


def use():
    return 'list [username]'

def desc():
    return 'see a list of a user\'s layouts'