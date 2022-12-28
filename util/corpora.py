from collections import Counter

def load(file: str='corpora/mt-quotes.txt') -> str:

    with open(file, 'r') as f:
        text = f.read()

    return text

def monograms():
    text = load()

    return dict(Counter(text).most_common())

def trigrams():
    text = load()

    return dict(Counter(''.join(x) for x in zip(text, text[1:], text[2:])).most_common())