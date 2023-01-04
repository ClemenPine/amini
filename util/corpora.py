import json

CORPUS = 'cache/mt-quotes'
NGRAMS = ['monograms', 'bigrams', 'trigrams']

def ngrams(n: int):
    path = f'{CORPUS}/{NGRAMS[n - 1]}.json'

    with open(path, 'r') as f:
        grams = json.load(f)

    return grams

def monograms():
    return ngrams(1)


def bigrams():
    return ngrams(2)


def trigrams():
    return ngrams(3)

def words():
    with open(f'{CORPUS}/words.json') as f:
        words = json.load(f)

    return words