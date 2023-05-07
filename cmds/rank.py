import os
import json
import logging

from discord import Message
from util import parser, corpora, analyzer, authors
from admins import ADMINS

RESTRICTED = False

def exec(message: Message):
    user = message.author.id
    user_name = authors.get_name(user).lower()
    # Check current user
    if user_name not in ADMINS:
        return 'Unauthorized'

    stat = parser.get_arg(message).lower()
    results = {}
    trigram = corpora.ngrams(3, id=message.author.id)
    for file in os.scandir('layouts'):
        print(f'Opening: {file.name}')
        with open(f'layouts/{file.name}', 'r') as f:
            data = json.load(f)

        name = data['name']
        stats = analyzer.trigrams(data, trigram)
        match stat:
            case 'sfb' | 'sfbs':
                results[name] = {
                    'sfb': stats["sfb"] / 2
                }
                stat = 'sfb'
            case 'sfs' | 'dsfb' | 'dsfbs':
                results[name] = {
                    'sfs': stats["dsfb-red"] + stats["dsfb-alt"]
                }
                stat = 'sfs'
            case _:
                return f'{stat} not supported'

    return '```' + '\n'.join(
        [f'{name} - {stat} = {result[stat]:.2%}' for name, result
            in sorted(results.items(), key=lambda x:x[1][stat])
            if result[stat] > 0.001][:10]
        ) + '```'
