import json
import glob
import random
from discord import Message

from util import parser

def exec(message: Message):
    sfb = parser.get_arg(message)

    res = []
    for file in glob.glob('layouts/*.json'):
        with open(file, 'r') as f:
            ll = json.load(f)

        if not all(x in ll['keys'] for x in sfb):
            continue

        fingers = set(ll['keys'][x]['finger'] for x in sfb)

        if len(fingers) == 1:
            res.append(ll['name'])

    random.shuffle(res)

    lines = [f'I found {len(res)} matches, here are a few of them:']
    
    lines.append('```')
    lines += list(sorted(res[:25], key=lambda x: x.lower()))
    lines.append('```')

    return '\n'.join(lines)


def use():
    return 'search [sfb/column]'

def desc():
    return 'find layouts with a particular set of sfbs'