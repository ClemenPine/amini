import os
import json
from collections import Counter
from more_itertools import windowed

FILE_NAME = 'mt-quotes'

NGRAMS = ['monograms', 'bigrams', 'trigrams']

def main():
    file = f'corpora/{FILE_NAME}.txt'
    cache = f'cache/{FILE_NAME}'

    os.mkdir(cache)

    with open(file, 'r') as f:
        words = f.read().split()

    # write ngrams
    for n in range(3):
        grams = [''.join(x) for x in windowed(' '.join(words), n=n+1)]
        grams = [x for x in grams if not ' ' in x]

        res = dict(Counter(grams).most_common())

        with open(f'{cache}/{NGRAMS[n]}.json', 'w') as f:
            f.write(json.dumps(res, indent=4))

    # write words
    res = dict(Counter(words).most_common())
    with open(f'{cache}/words.json', 'w') as f:
        f.write(json.dumps(res, indent=4))
        
if __name__ == '__main__':
    main()