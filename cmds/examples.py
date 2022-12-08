import humanize
from discord import Message
from collections import Counter
from more_itertools import windowed

from util import corpora, parser

def exec(message: Message):
    string = parser.get_arg(message)
    words = corpora.load().lower().split()

    chunk_size = string.count(' ') + 1

    counts = Counter()
    for item in [' '.join(x) for x in windowed(words, n=chunk_size)]:
        if string in item:
            counts.update([item])

    examples = []
    total = 0

    for (item, count) in counts.most_common(10):
        total += count
        examples.append(f'{item:<15} {"(" + str(count) + ")":>6}')

    if not examples:
        return f'Error: `{string}` does not appear anywhere in MT Quotes'

    perc = total / len(words)

    res = [f'Examples of `{string}` in MT Quotes:']
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