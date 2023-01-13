import json

from util import analyzer, authors, corpora
from util.consts import JSON

def to_string(ll: JSON, id: int):
    author = authors.get_name(ll['user'])

    max_width = max(x['col'] for x in ll['keys'].values()) + 1
    max_height = max(x['row'] for x in ll['keys'].values()) + 1

    matrix = [[' ']*max_width for _ in range(max_height)]
    
    for char, info in ll['keys'].items():
        row = info['row']
        col = info['col']

        matrix[row][col] = char

    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            char = matrix[i][j]

            if j == 0:
                matrix[i][j] = '  ' + char
            elif j == 4:
                matrix[i][j] += ' '

    if ll['board'] == 'stagger':
        matrix[1][0] = ' ' + matrix[1][0]
        matrix[2][0] = '  ' + matrix[2][0]
    elif ll['board'] == 'angle':
        matrix[2][0] = ' ' + matrix[2][0]

    monogram = corpora.ngrams(1, id=id)
    trigram = corpora.ngrams(3, id=id)
    
    stats = analyzer.trigrams(ll, trigram)
    use = analyzer.use(ll, monogram)

    matrix_str = '\n'.join(' '.join(x) for x in matrix)

    with open('likes.json', 'r') as f:
        likes = json.load(f)

    if ll['name'] in likes:
        likes = len(likes[ll['name']])
    else:
        likes = 0

    if likes == 1:
        like_string = 'like'
    else:
        like_string = 'likes'

    res = (
        f'```\n'
        f'{ll["name"]} ({author}) ({likes} {like_string})\n'
        f'{matrix_str}\n'
        f'\n'
        f'{corpora.get_corpus(id).upper()}:\n'
        f' {"Alt:":>5} {stats["alternate"]:>6.2%}\n' 
        f' {"Rol:":>5} {stats["roll-in"] + stats["roll-out"]:>6.2%}'
        f'   (In/Out: {stats["roll-in"]:>6.2%} | {stats["roll-out"]:>6.2%})\n'
        # f'   (In: {stats["roll-in"]:>6.2%} Out: {stats["roll-out"]:>6.2%})\n'
        f' {"One:":>5} {stats["oneh-in"] + stats["oneh-out"]:>6.2%}'
        f'   (In/Out: {stats["oneh-in"]:>6.2%} | {stats["oneh-out"]:>6.2%})\n'
        # f'   (In: {stats["oneh-in"]:>6.2%} Out: {stats["oneh-out"]:>6.2%})\n'
        f' {"Red:":>5} {stats["redirect"] + stats["bad-redirect"]:>6.2%}'
        f'   (Bad: {stats["bad-redirect"]:>9.2%})\n'
        f'  SFB/DFB: {stats["sfb"] / 2:.2%} | {stats["dsfb-red"] + stats["dsfb-alt"]:.2%}\n'
        f'  LH/RH: {use["LH"]:.2%} | {use["RH"]:.2%}'
        f'```\n'
    )

    return res   