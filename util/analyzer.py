import json
from typing import Dict

def trigrams(ll, grams: Dict[str, int]):
    table = get_table()

    counts = {x: 0 for x in list(table.values()) + ['sfR', 'unknown']}

    for gram, count in grams.items():
        if ' ' in gram:
            continue

        key = '-'.join(ll['keys'][x]['finger'] for x in gram if x in ll['keys'])

        if len(set(gram)) < len(gram):
            gram_type = 'sfR'
        elif key in table:
            gram_type = table[key]
        else:
            gram_type = 'unknown'

        counts[gram_type] += count

    total = sum(counts.values())
    for stat in counts:
        counts[stat] /= total

    return counts


def get_table(file: str='table.json'):
    with open(file, 'r') as f:
        table = json.load(f)

    return table