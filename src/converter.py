from typing import Dict, List

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

    curr = char
    while TO[curr] != FROM[char]:
        curr = [k for k in FROM if FROM[k] == TO[curr]][0]
        cycles.append(curr)

    return cycles


def convert(FROM: kb.Layout, TO: kb.Layout) -> List[str]:
    A = load(FROM)
    B = load(TO)

    if set(A.values()) != set(B.values()):
        return 'NOSHAPE', None
    elif set(A.keys()) != set(B.keys()):
        return 'NOKEY', None

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

    final = [f'a `{"".join(x)}` swap' for x in swaps]
    final += [f'a `{"".join(x)}` cycle' for x in cycles]

    return 'OK', final 
