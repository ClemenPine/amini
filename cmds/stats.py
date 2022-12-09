import json
import glob
from discord import Message

def exec(message: Message):
    files = glob.glob('layouts/*.json')

    with open('authors.json', 'r') as f:
        authors = json.load(f)
    
    return '\n'.join([
        '```',
        '--- AMINI STATS ---',
        f'Layouts: {len(files)}',
        f'Authors: {len(authors)}'
        '```'
    ])

def use():
    return 'stats'

def desc():
    return 'see the global stats'