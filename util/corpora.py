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
    return ngrams(1)


def bigrams():
    return ngrams(2)


def trigrams():
    return ngrams(3)