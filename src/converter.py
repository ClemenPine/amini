from typing import Dict

import kb

def load(ll: kb.Layout):
    kmap = {}

    lines = ll.matrix.split('\n')

    for row, line in enumerate(lines):
        for finger, key in enumerate(line.split()):
            kmap[key] = f'{row}-{finger}'

    return kmap    


def get_cycle(char: str, FROM: Dict[str, str], TO: Dict[str, str]) -> str:
    cycles = [char]

    try:
        curr = char
        while TO[curr] != FROM[char]:
            curr = [k for k in FROM if FROM[k] == TO[curr]][0]
            cycles.append(curr)
    except:
        return []

    return cycles


def convert(FROM: kb.Layout, TO: kb.Layout):
    A = load(FROM)
    B = load(TO)

    found = []

    swaps = []
    cycles = []

    for key in A:
        if key in found:
            continue

        cycle = get_cycle(key, A, B)
        found += cycle

        if len(cycle) == 2:
            swaps.append(cycle)
        elif len(cycle) > 2:
            cycles.append(cycle)

    swaps = sorted(swaps, key=lambda x: len(x))
    cycles = sorted(cycles, key=lambda x: len(x))

    res = [f'a `{"".join(x)}` swap' for x in swaps]
    res += [f'a `{"".join(x)}` cycle' for x in cycles]

    return f'do {", ".join(res[:-1])} and {res[-1]}' 
