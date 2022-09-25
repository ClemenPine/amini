import re
import humanize
from more_itertools import ilen
from typing import List

import mt

def odds(string: str, *, words: List[str]):
    text = f' {" ".join(words)} '
    size = len(text)

    parts = string.split(' ')
        
    if len(parts) == 1:
        count = len(re.findall(string, text))

        if count:
            res = size // count
        else:
            res = 0

    else:
        start = ilen(w for w in words if w.endswith(parts[0]))
        end = ilen(w for w in words if w.startswith(parts[-1]))

        if all(x in words for x in parts[1:-1]):
            prob = start * end * size**len(parts[1:-1])
        else:
            prob = 0

        if prob:
            res = size ** len(parts) // prob
        else:
            res = 0

    return res 


def find(input: str):
    args = input.split('+')
    strings = [x.strip().replace('_', ' ') for x in args]

    res = {}
    for name in mt.languages:
        lang = mt.load_language(name)

        num = 0
        for string in strings:
            new = odds(string, words=lang['words'])

            if not num:
                num = new
            elif not new:
                pass
            else:
                num = (num * new) / (num + new)

        num //= min(5, len(min(strings, key=lambda x: len(x))))
        res[name] = humanize.intword(num, '%.0f')

    max_name = len(max(res.keys(), key=lambda x: len(x)))
    max_num = len(max(res.items(), key=lambda x: len(x[1]))[1])

    out = " + ".join(f'"{x}"' for x in strings)

    final = f'Here are the odds for {out}\n'
    final += '```\n'

    for name, num in res.items():
        left = format(f'{name}', f'>{max_name + 2}')
        right = format(f'{num} to 1', f'>{max_num + 5}')

        final += f'- {left} {" "*3} {right}\n'

    final += '```\n'
    return final