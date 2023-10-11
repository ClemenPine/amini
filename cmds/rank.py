import os
import json
import logging
import argparse

from discord import Message
from util import parser, corpora, analyzer, authors, cache
from admins import ADMINS

RESTRICTED = False

def exec(message: Message):
    user = message.author.id
    user_name = authors.get_name(user).lower()
    corpus = corpora.get_corpus(user)
    # Check current user
    # if user_name in ADMINS:
        # length = 100
    # else:
        # length = 15

    length = 15

    try:
        kwargs = __Parser.get_kwargs(parser.get_arg(message))
    except ValueError:
        return 'Error: Invalid starting index'
    stat = kwargs['stat_name']
    start = kwargs['start_index']
    sort_asc = kwargs['min']
    sort_desc = kwargs['max']
    if sort_asc and sort_desc:
        return 'Error: Cannot rank ascending and descending altogether'
    use_override_reverse = sort_asc or sort_desc
    override_reverse = sort_desc

    if stat == '':
        return '```\n' + \
            'Supported rank stats:\n' + \
            'alt sfb sfs red oneh inroll outroll roll inrollratio outrollratio inrolltal outrolltal rolltal' + \
            '```'
    results = {}
    reverse = False
    percent = True
    # trigram = corpora.ngrams(3, id=message.author.id)
    for file in os.scandir('cache'):
        # print(f'Opening: {file.name}')
        # with open(f'layouts/{file.name}', 'r') as f:
        #     data = json.load(f)

        # name = data['name']

        # stats = analyzer.trigrams(data, trigram)

        name = file.name.split(".json")[0]
        stats = cache.get(name, corpus)

        # print(f"Name: {name}, Corpus: {corpus}")
        try:
            match stat:
                case 'alt' | 'alts' | 'alternate':
                    stat = 'alt'
                    results[name] = {
                        stat: stats["alternate"]
                    }
                    reverse = True
                case 'sfb' | 'sfbs':
                    stat = 'sfb'
                    results[name] = {
                        stat: stats["sfb"] / 2
                    }
                case 'sfs' | 'dsfb' | 'dsfbs':
                    stat = 'sfs'
                    results[name] = {
                        stat: stats["dsfb-red"] + stats["dsfb-alt"]
                    }
                case 'red' | 'redirect' | 'redirects':
                    stat = 'redirect'
                    results[name] = {
                        stat: stats["redirect"] + stats["bad-redirect"]
                    }
                case 'oneh' | 'onehand' | 'onehands':
                    stat = 'onehand'
                    results[name] = {
                        stat: stats["oneh-in"] + stats["oneh-out"]
                    }
                    reverse = True
                case 'inroll' | 'inrolls' | 'roll-in':
                    stat = 'roll-in'
                    results[name] = {
                        stat: stats["roll-in"]
                    }
                    reverse = True
                case 'outroll' | 'outrolls' | 'roll-out':
                    stat = 'roll-out'
                    results[name] = {
                        stat: stats["roll-out"]
                    }
                    reverse = True
                case 'roll' | 'rolls' | 'roll-total':
                    stat = 'roll-total'
                    results[name] = {
                        stat: stats["roll-in"] + stats["roll-out"]
                    }
                    reverse = True
                case 'inrollratio' | 'roll-in-ratio':
                    stat = 'roll-in-ratio'
                    results[name] = {
                        stat: stats["roll-in"] / stats["roll-out"]
                    }
                    reverse = True
                    percent = False
                case 'outrollratio' | 'roll-out-ratio':
                    stat = 'roll-out-ratio'
                    results[name] = {
                        stat: stats["roll-out"] / stats["roll-in"]
                    }
                    reverse = True
                    percent = False
                case 'inrolltal' | 'inrolltals':
                    stat = 'inrolltal'
                    results[name] = {
                        stat: stats["roll-in"] + stats["oneh-in"]
                    }
                    reverse = True
                case 'outrolltal' | 'outrolltals':
                    stat = 'outrolltal'
                    results[name] = {
                        stat: stats["roll-out"] + stats["oneh-out"]
                    }
                    reverse = True
                case 'rolltal' | 'rolltals' | 'rolltotal':
                    stat = 'rolltal'
                    results[name] = {
                        stat: stats["roll-in"] + stats["oneh-in"] + stats["roll-out"] + stats["oneh-out"]
                    }
                    reverse = True
                case _:
                    return f'{stat} not supported'
        except:
            print(f"{name}: Error computing {stat}")

    if use_override_reverse:
        reverse = override_reverse
    sorted_results = sorted(results.items(), key=lambda x: x[1][stat], reverse=reverse)

    if percent: 
        return '```\n' + f'{corpus.upper()}\n' + '\n'.join(
            [f'{index+start}: {value}' for index, value
                in enumerate([f'{result[stat]:.2%} -- {name}' for name, result
                in sorted_results
                if result[stat] > 0.001][start:start+length % len(sorted_results)])
            ]
            ) + '```'
    else:
        return '```\n' + f'{corpus.upper()}\n' + '\n'.join(
            [f'{index+start}: {value}' for index, value
                in enumerate([f'{result[stat]:.3} -- {name}' for name, result
                in sorted_results
                if result[stat] > 0.001][start:start+length % len(sorted_results)])
            ]
            ) + '```'

class __Parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('start_index', nargs='?', default=0)
    kw_parser = argparse.ArgumentParser()
    kw_parser.add_argument('--min', action='store_true')
    kw_parser.add_argument('--max', action='store_true')

    @classmethod
    def get_kwargs(cls, command: str) -> dict[str | int | bool]:
        command: list[str] = command.lower().split()
        if not command:
            return {"stat_name": "", "start_index": 0, "min": False, "max": False}
        stat = command[0]
        if len(command) == 1:
            return {"stat_name": stat, "start_index": 0, "min": False, "max": False}
        if len(command) > 1:
            args, remaining = cls.parser.parse_known_args(command[1:])
            args.start_index = int(args.start_index)
            kwargs, unknown = cls.kw_parser.parse_known_args(remaining)
            return {"stat_name": stat} | vars(args) | vars(kwargs)

