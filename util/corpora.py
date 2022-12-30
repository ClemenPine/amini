import json
from collections import Counter
from more_itertools import windowed

def load(file: str='corpora/mt-quotes.txt') -> str:

    with open(file, 'r') as f:
        text = f.read()

    return text

def ngrams(n: int):
    text = load()

    ngrams = [''.join(x) for x in windowed(text, n=n)]
    return dict(Counter(ngrams).most_common())


def monograms():
    with open('cache/akl/monograms.json') as f:
        grams = json.load(f)

    return grams
    # return ngrams(1)


def bigrams():
    with open('cache/akl/bigrams.json') as f:
        grams = json.load(f)

    return grams
    # return ngrams(2)


def trigrams():
    with open('cache/akl/trigrams.json') as f:
        grams = json.load(f)

    return grams
    # return ngrams(3)

def words():
    with open('cache/akl/words.json') as f:
        words = json.load(f)

    return words