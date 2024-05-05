from discord import Message
from util import corpora, memory, parser

def exec(message: Message):
    args = parser.get_args(message)
    name, query = args[0], args[1:]
    ntype = len(query[0]) if len(query) > 0 else None

    if not name:
        return "Please provide a layout"

    if not query or ntype != 2:
        return "Please provide valid finger values (e.g., LI)"

    if len(query) > len(corpora.NGRAMS):
        return "Please provide no more than 3 finger values"

    ll = memory.find(name)
    if not ll:
        return f'Error: couldn\'t find any layout named `{name}`'
    
    allowed_fingers = set(["LI", "LM", "LR", "LP", "RI", "RM", "RR", "RP", "LT", "RT", "TB"])

    if not all(finger in allowed_fingers for finger in query):
        return "Please provide valid finger values (e.g., LI)"
    
    ngrams = corpora.ngrams(len(query), id=message.author.id)
    freq = 0
    total = sum(ngrams.values())
    lines = []
    
    for gram, count in ngrams.items():
        gram = gram.lower()
        if len(set(gram)) != len(gram):
            continue

        fingers = '-'.join(query)
        key = '-'.join([ll.keys[x].finger for x in gram if x in ll.keys])
        
        if fingers in key:
            freq += count
            lines.append(f'{gram:<5} {count / total:.3%}')

    return '\n'.join([
        '```',
        f'Top 10 {ll.name} Patterns for {fingers}:',
        *lines[:10],
        f'Total {freq / total:.3%}',
        '```'
    ])

def use():
    return 'pattern [layout name] [finger string]'

def desc():
    return 'see the most common pattern for a given finger string (e.g., RM LI or LP LR LM)'
