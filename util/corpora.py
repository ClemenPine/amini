import json

CORPUS = 'mt-quotes'
NGRAMS = ['monograms', 'bigrams', 'trigrams']

def ngrams(n: int, *, id: int=0):
    file = get_corpus(id)
    path = f'cache/{file}/{NGRAMS[n - 1]}.json'

    with open(path, 'r') as f:
        grams = json.load(f)

    return grams

def monograms():
    return ngrams(1)

def bigrams():
    return ngrams(2)

def trigrams():
    return ngrams(3)

def words(id: int=0):
    file = get_corpus(id)
    with open(f'cache/{file}/words.json') as f:
        words = json.load(f)

    return words

def get_corpus(id: int):
    with open('corpora.json', 'r') as f:
        prefs = json.load(f)

    if str(id) in prefs:
        file = prefs[str(id)]
    else:
        file = CORPUS

    return file