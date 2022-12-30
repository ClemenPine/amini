import json
from collections import Counter
from itertools import islice
from more_itertools import windowed

CORPUS = 'cache/akl'

def load(file: str='corpora/mt-quotes.txt') -> str:

    with open(file, 'r') as f:
        text = f.read()

    return text

def ngrams(n: int):
    text = load()

    ngrams = [''.join(x) for x in windowed(text, n=n)]
    return dict(Counter(ngrams).most_common())


def monograms():
    with open(f'{CORPUS}/monograms.json') as f:
        grams = json.load(f)

    return grams


def bigrams():
    with open(f'{CORPUS}/bigrams.json') as f:
        grams = json.load(f)

    return grams


def trigrams():
    with open(f'{CORPUS}/trigrams.json') as f:
        grams = json.load(f)

    return grams

def words():
    with open(f'{CORPUS}/words.json') as f:
        words = json.load(f)

    return words