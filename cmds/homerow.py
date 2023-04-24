import glob
import json
import random
from discord import Message

from util import parser

def exec(message: Message):
    row = ''.join(parser.get_args(message))
    lines = []
    for file in glob.glob('layouts/*.json'):
        with open(file, 'r') as f:
            ll = json.load(f)

        keys = sorted(ll['keys'].items(), key=lambda k: (k[1]['row'], k[1]['col']))
        homerow = ''.join(k for k,v in keys if v['row'] == 1)

        it = iter(homerow)
        if all(i in it for i in row):
            lines.append(ll['name'])

    if len(lines) < 25:
        res = lines
    else:
        res = random.sample(lines, k=25)

    res = list(sorted(res, key=lambda x: x.lower()))

    return '\n'.join([f'I found {len(lines)} matches, here are a few', '```'] + res + ['```'])


def use():
    return 'homerow [string]'

def desc():
    return 'search for layouts with a particular string in homerow'
