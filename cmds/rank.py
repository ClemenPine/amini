import os
import json
import logging

from discord import Message
from util import parser, corpora, analyzer, authors, cache
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
    # trigram = corpora.ngrams(3, id=message.author.id)
    for file in os.scandir('cache'):
        # print(f'Opening: {file.name}')
        # with open(f'layouts/{file.name}', 'r') as f:
        #     data = json.load(f)

        # name = data['name']

        # stats = analyzer.trigrams(data, trigram)

        name = file.name.split(".json")[0]
        corpus = corpora.get_corpus(user)
        stats = cache.get(name, corpus)

        # print(f"Name: {name}, Corpus: {corpus}")

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
            case 'inroll' | 'roll-in':
                results[name] = {
                    'roll-in': stats["roll-in"]
                }
                stat = 'roll-in'
            case 'outroll' | 'roll-out':
                results[name] = {
                    'roll-out': stats["roll-out"]
                }
                stat = 'roll-out'
            # case 'rollinratio' | 'roll-in-ratio':
            #     results[name] = {
            #         'roll-in-ratio': stats["roll-out"] / stats["roll-in"]
            #     }
            #     stat = 'roll-in-ratio'
            case _:
                return f'{stat} not supported'

    return '```' + '\n'.join(
        [f'{name} - {stat} = {result[stat]:.2%}' for name, result
            in sorted(results.items(), key=lambda x:x[1][stat])
            if result[stat] > 0.001][:15]
        ) + '```'
