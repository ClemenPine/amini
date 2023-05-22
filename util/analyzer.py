import json
from typing import Dict

def use(ll, grams: Dict[str, str]):
    fingers = {}
    
    for gram, count in grams.items():
        if not gram in ll['keys']:
            continue

        finger = ll['keys'][gram]['finger']
        
        if not finger in fingers:
            fingers[finger] = 0

        fingers[finger] += count

    total = sum(fingers.values())
    for finger in fingers:
        fingers[finger] /= total

    fingers['LH'] = sum(fingers[x] for x in fingers if x[0] in 'L')
    fingers['RH'] = sum(fingers[x] for x in fingers if x[0] in 'RT')


    # fingers['LH'] = (
    #     fingers['LI'] + 
    #     fingers['LM'] + 
    #     fingers['LR'] +
    #     fingers['LP']
    # )

    # fingers['RH'] = (
    #     fingers['RI'] + 
    #     fingers['RM'] + 
    #     fingers['RR'] +
    #     fingers['RP']
    # )

    return fingers



def trigrams(ll, grams: Dict[str, int]):
    table = get_table()

    counts = {x: 0 for x in list(table.values()) + ['sfR', 'unknown']}

    for gram, count in grams.items():
        if ' ' in gram:
            continue

        key = '-'.join(ll['keys'][x]['finger'] for x in gram if x in ll['keys'])
        key = key.replace('TB', 'RT')

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