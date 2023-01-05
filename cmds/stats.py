import json
import glob
from collections import Counter
from discord import Message

def exec(message: Message):
    files = glob.glob('layouts/*.json')

    with open('authors.json', 'r') as f:
        authors = json.load(f)
    
    with open('likes.json', 'r') as f:
        likes = json.load(f)

    with open('corpora.json', 'r') as f:
        corpora = json.load(f)

    most_liked = list(sorted(likes.items(), key=lambda x: len(x[1]), reverse=True))
    top_corpora = Counter(corpora.values()).most_common()

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
        '',
        f'Top Corpora:',
        f'    {top_corpora[0][0]:<15} ({top_corpora[0][1]} users)',
        f'    {top_corpora[1][0]:<15} ({top_corpora[1][1]} users)',
        f'    {top_corpora[2][0]:<15} ({top_corpora[2][1]} users)',
        '```'
    ])

def use():
    return 'stats'

def desc():
    return 'see the global stats'