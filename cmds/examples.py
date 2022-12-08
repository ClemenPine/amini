import humanize
from discord import Message
from collections import Counter
from more_itertools import windowed

from util import corpora, parser
from util.consts import PUNCT

def exec(message: Message):
    part = parser.get_arg(message)
    words = corpora.load().lower().split()

    if not any(x in PUNCT for x in part):
        words = [x.strip(PUNCT) for x in words]

    chunk_size = part.count(' ') + 1

    counts = Counter()
    for item in [' '.join(x) for x in windowed(words, n=chunk_size)]:
        if part in item:
            counts.update([item])

    examples = []
    total = 0

    for (item, count) in counts.most_common(10):
        total += count
        examples.append(f'{item:<15} {"(" + str(count) + ")":>6}')

    if not examples:
        return f'Error: `{part}` does not appear anywhere in MT Quotes'

    perc = total / len(words)

    res = [f'Examples of `{part}` in MT Quotes:']
    res.append('```')
    
    res.append(f'{humanize.intcomma(total)} / {humanize.intcomma(len(words))} words ({perc:.2%})')
    res.append('')
    res += examples
    
    res.append('```')
    return '\n'.join(res)

def use():
    return 'examples [some_str]'

def desc():
    return 'find common examples of an ngram from MT-Quotes'