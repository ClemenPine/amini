from discord import Message

from util import corpora, memory, parser, analyzer
from util.analyzer import TABLE

def exec(message: Message):
    name = parser.get_arg(message)
    ll = memory.find(name.lower())

    trigrams = corpora.ngrams(3, id=message.author.id)
    total = sum(trigrams.values())

    lines = []
    for gram, count in trigrams.items():
        if len(set(gram)) != len(gram): # ignore repeats
            continue

        key = '-'.join([ll.keys[x].finger for x in gram if x in ll.keys])

        if key in TABLE and TABLE[key].startswith('dsfb'):
            lines.append(f'{gram:<5} {count / total:.3%}')

    return '\n'.join(['```', f'Top 10 {ll.name} SFS:'] + lines[:10] + ['```'])

def use():
    return 'sfs [layout name]'

def desc():
    return 'see the worst sfs for a particular layout'