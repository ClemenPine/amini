from collections import Counter

def trigrams(file: str):
    with open(file, 'r') as f:
        text = '_'.join(f.read().split())

    return dict(Counter(''.join(x) for x in zip(text, text[1:], text[2:])).most_common())