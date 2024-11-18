from discord import Message
from util import corpora, memory, parser

def exec(message: Message):
    args = parser.get_args(message)
    name, query = args[0], args[1:]

    if not name:
        return "Please provide a layout"

    if not query:
        return "Please provide finger values (e.g., LI, _, LI|RR)"

    if len(query) > len(corpora.NGRAMS):
        return "Please provide no more than 3 finger values"

    ll = memory.find(name)
    if not ll:
        return f'Error: couldn\'t find any layout named `{name}`'

    allowed_fingers = {"LI", "LM", "LR", "LP", "RI", "RM", "RR", "RP", "LT", "RT", "TB", "_"}

    if not all(all(finger in allowed_fingers for finger in node.split('|')) for node in query):
        return "Please provide valid finger values (e.g., LI, _, LI|RR)"

    ngrams = corpora.ngrams(len(query), id=message.author.id)
    freq = 0
    total = sum(ngrams.values())
    ngrams = {}

    for gram, count in ngrams.items():
        gram = gram.lower()
        if len(set(gram)) != len(gram):
            continue

        fingers = [list(allowed_fingers) if finger == "_" else [finger.split("|")] for finger in query]
        keys = [ll.keys[x].finger for x in gram if x in ll.keys]

        if all(key in finger for key, finger in zip(keys,fingers)):
            ngrams[gram] = ngrams.get(gram, 0) + count
            freq += count

    ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)

    return '\n'.join([
        '```',
        f'Top 10 {ll.name} Patterns for {'-'.join(query)}:'] +
        [f'{gram:<6} {count / total:.3%}' for (gram, count), _ in zip(ngrams, range(10))] +
        [f'Total {freq / total:.3%}',
        '```'
    ])

def use():
    return 'pattern [layout name] [finger string]'

def desc():
    return 'see the most common pattern for a given finger string (e.g., RM LI|RR or LP _ LM)'
