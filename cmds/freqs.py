import re
from discord import Message
from util import corpora, parser

RESTRICTED = True

def get_reverse(ngram):
    return ngram[::-1]

def calculate_freq(item, ngrams):
    pattern = re.compile(item.replace('.', '\.').replace('_', '.'))
    count = sum(value for key, value in ngrams.items() if pattern.search(key))
    return count / sum(ngrams.values())

def exec(message: Message):
    id = message.author.id
    query = parser.get_args(message)

    if not query or not (1 <= (ntype := len(query[0])) <= 3) or len(query) > 6:
        return 'Please provide 1 to 6 ngrams of length 1-3 characters'

    ngrams = corpora.ngrams(ntype, id=id)
    corpus = corpora.get_corpus(id)

    processed_ngrams = set()
    total_freq = 0
    total_ngrams = []
    res = ['```', f'{corpus.upper()}']

    for item in query:
        if len(item) != ntype:
            return 'All ngrams must be the same length'

        reverse = get_reverse(item)

        if item in processed_ngrams or (ntype > 1 and reverse in processed_ngrams):
            continue

        processed_ngrams.update({item, reverse})

        freq_original = calculate_freq(item, ngrams)
        total_freq += freq_original
        
        if ntype > 1:
            freq_reverse = calculate_freq(reverse, ngrams)

            res.extend([
                f'{item} + {reverse}: {freq_original + freq_reverse:.2%}',
                f'  {item}: {freq_original:.2%}',
                f'  {reverse}: {freq_reverse:.2%}'
            ])
            total_freq += freq_reverse
            total_ngrams.append(f'{item} + {reverse}')
        elif ntype == 1:
            res.append(f'{item}: {freq_original:.2%}')
            total_ngrams.append(f'{item}')

    if total_freq == 0:
        return f'`{" ".join(query)}` not found in corpus `{corpus}`'

    if len(query) == 1 or all(item == query[0] or get_reverse(item) == query[0] for item in query):
        res.append('```')
    elif len(query) > 1:
        res.extend([f'{" + ".join(total_ngrams)}: {total_freq:.2%}', '```'])
    return '\n'.join(res)