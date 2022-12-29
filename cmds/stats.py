import json
import glob
from discord import Message

def exec(message: Message):
    files = glob.glob('layouts/*.json')

    with open('authors.json', 'r') as f:
        authors = json.load(f)
    
    with open('likes.json', 'r') as f:
        likes = json.load(f)

    most_liked = list(sorted(likes.items(), key=lambda x: len(x[1]), reverse=True))

    return '\n'.join([
        '```',
        '--- AMINI STATS ---',
        f'Layouts: {len(files)}',
        f'Authors: {len(authors)}',
        '',
        f'Most liked layouts:',
        f'    {most_liked[0][0]:<15} ({len(likes[most_liked[0][0]])} likes)',
        f'    {most_liked[1][0]:<15} ({len(likes[most_liked[1][0]])} likes)',
        f'    {most_liked[2][0]:<15} ({len(likes[most_liked[2][0]])} likes)',
        f'    {most_liked[3][0]:<15} ({len(likes[most_liked[3][0]])} likes)',
        f'    {most_liked[4][0]:<15} ({len(likes[most_liked[4][0]])} likes)',
        '```'
    ])

def use():
    return 'stats'

def desc():
    return 'see the global stats'