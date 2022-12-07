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

    res = [f'Examples of `{string}` in MT Quotes:']
    res.append('```')
    for (item, count) in counts.most_common(10):
        res.append(f'{item:<15} {"(" + str(count) + ")":>6}')

    res.append('```')

    return '\n'.join(res)

def use():
    return 'examples [some_str]'

def desc():
    return 'find common examples of an ngram from MT-Quotes'