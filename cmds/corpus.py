import glob
import json
from discord import Message

from util import parser

def exec(message: Message):
    arg = parser.get_arg(message).lower()

    if not f'cache/{arg}/' in glob.glob('cache/*/'):
        return f'The corpus `{arg}` doesn\'t exist.'

    with open('corpora.json', 'r') as f:
        prefs = json.load(f)

    prefs[str(message.author.id)] = arg

    with open('corpora.json', 'w') as f:
        f.write(json.dumps(prefs, indent=4))

    return f'Your corpus preference has been changed to `{arg}`.'    

def use():
    return 'corpus [corpus_name]'

def desc():
    return 'set your preferred corpus'