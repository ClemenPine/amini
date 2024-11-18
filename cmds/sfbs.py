from discord import Message

from util import corpora, memory, parser

def exec(message: Message):
    name = parser.get_arg(message)
    ll = memory.find(name.lower())

    bigrams = corpora.ngrams(2, id=message.author.id)
    total = sum(bigrams.values())

    lines = []
    sfb_total = 0
    for gram, count in bigrams.items():
        gram = gram.lower()
        if len(set(gram)) != len(gram): # ignore repeats
            continue

        fingers = [ll.keys[x].finger for x in gram if x in ll.keys]

        if len(set(fingers)) != len(fingers):
            lines.append(f'{gram:<5} {count / total:.3%}')
            sfb_total += count

        if len(lines) == 10:
            break

    lines.append(f"Total: {sfb_total / total: .3%}")

    return '\n'.join(['```', f'Top 10 {ll.name} SFBs:'] + lines + ['```'])

def use():
    return 'sfbs [layout name]'

def desc():
    return 'see the worst sfbs for a particular layout'
