import glob
import json
import random
from discord import Message, ChannelType

from util import parser

def exec(message: Message):
    row = ''.join(parser.get_args(message))
    lines = []
    for file in glob.glob('layouts/*.json'):
        with open(file, 'r') as f:
            ll = json.load(f)

        keys = sorted(ll['keys'].items(), key=lambda k: (k[1]['row'], k[1]['col']))
        homerow = ''.join(k for k,v in keys if v['row'] == 1)

        if row.startswith('"') and row.endswith('"'):
            if row.strip('"') in homerow or "".join(reversed(row.strip('"'))) in homerow:
                lines.append(ll['name'])
        else:
            if all(i in homerow for i in row):
                lines.append(ll['name'])

    is_dm = message.channel.type == ChannelType.private

    if is_dm:
        res = lines
        res_len = len(lines)
    else:
        if len(lines) < 20:
            res = lines
            res_len = len(lines)
            if res_len < 1:
                return "No matches found"
        else:
            res = random.sample(lines, k=20)
            res_len = 20

    res = list(sorted(res, key=lambda x: x.lower()))
    note = "" if is_dm else f", here are {res_len} of them"

    return '\n'.join([f'I found {len(lines)} matches{note}', '```'] + res + ['```'])


def use():
    return 'homerow [string]'

def desc():
    return 'search for layouts with a particular string in homerow'
