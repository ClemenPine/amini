import glob
from discord import Message

def exec(message: Message):
    files = glob.glob('layouts/*.json')
    
    return '\n'.join([
        '```',
        '--- AMINI STATS ---',
        f'Layouts: {len(files)}',
        '```'
    ])

def use():
    return 'stats'

def desc():
    return 'see the global stats'