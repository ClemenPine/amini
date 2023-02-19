import glob
import json
import random
from discord import Message

from util import parser

def exec(message: Message):
    rows = parser.get_args(message)

    lines = []
    for file in glob.glob('layouts/*.json'):
        with open(file, 'r') as f:
            ll = json.load(f)

        homerow = ''.join(k for k in ll['keys'] if ll['keys'][k]['row'] == 1)
        homerow = homerow[0:4] + homerow[6:10] # ignore center columns
        if all(
            row in homerow or
            row in homerow[::-1] for row in rows
        ):
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
