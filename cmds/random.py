import json
import glob
import random
from discord import Message

from util import layout

def exec(message: Message):
    files = glob.glob('layouts/*.json')

    with open(random.choice(files), 'r') as f:
        ll = json.load(f)

    return layout.to_string(ll)
