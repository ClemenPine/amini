import json
import glob
import random
from discord import Message, ChannelType

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

    res_len = len(res) if len(res) < 20 else 20
    if res_len < 1:
        return 'No matches found'

    is_dm = message.channel.type is ChannelType.private
    lines = [f'I found {len(res)} matches, here are {"all" if is_dm else res_len} of them:']

    lines.append('```')
    lines += list(sorted(res[:None if is_dm else res_len], key=lambda x: x.lower()))
    lines.append('```')

    return '\n'.join(lines)


def use():
    return 'search [sfb/column]'

def desc():
    return 'find layouts with a particular set of sfbs'
