from typing import Dict
from itertools import zip_longest
from dataclasses import dataclass

import analyzer, corpora

@dataclass
class Layout:
    name: str
    matrix: str
    keymap: Dict[str, str]

    def __init__(self, matrix: str, *, name: str):
        self.name = name
        self.matrix = matrix

        self.keymap = {}
        rows = matrix.split('\n')

        has_thumb = len(rows[-1].split()) < 4

        i = 0
        for col in zip_longest(*rows, fillvalue=' '):
            keys = [x for x in col if x != ' ']

            for key in keys:
                finger = get_finger(i)
                self.add(key, finger)

            if has_thumb and col[-1] != ' ':
                if i < 5:
                    finger = 'LT'
                else:
                    finger = 'RT'

                self.add(key, finger)

            if keys:
                i += 1

        if '_' in self.keymap:
            return

        if 'LT' in self.keymap.values():
            self.add('_', 'RT')
        elif 'RT' in self.keymap.values():
            self.add('_', 'LT')
        else:
            left, right = 0, 0

            for key, finger in self.keymap.items():
                if key in 'bcdfghjklmnpqrstvwxz':
                    if finger[0] == 'L':
                        left += 1
                    elif finger[0] == 'R':
                        right += 1

            if right > left:
                self.add('_', 'RT')
            else:
                self.add('_', 'LT')


    def add(self, char: str, finger: str):
        self.keymap[char] = finger
        # self.keymap[shift(char)] = finger


    def type(self, string: str):
        for ch in string:
            if ch in self.keymap:
                yield self.keymap[ch]
            else:
                yield '??'


    def __str__(self):
        data = corpora.trigrams('corpora/mt-quotes.txt')
        stats = analyzer.trigrams(self, data)

        res = (
            f'```\n'
            f'{self.name}\n'
            f'{self.matrix}\n'
            f'\n'
            f'{"Alt:":>5} {stats["alternate"]:>6.2%}\n' 
            f'{"Roll:":>5} {stats["roll-in"] + stats["roll-out"]:>6.2%}'
            f'   (In: {stats["roll-in"]:>6.2%} Out: {stats["roll-out"]:>6.2%})\n'
            f'{"One:":>5} {stats["oneh-in"] + stats["oneh-out"]:>6.2%}'
            f'   (In: {stats["oneh-in"]:>6.2%} Out: {stats["oneh-out"]:>6.2%})\n'
            f'{"Red:":>5} {stats["redirect"]:>6.2%}\n'
            '\n'
            f'SFB: {stats["sfb"] / 2:.2%}\n' 
            f'DFB: {stats["dsfb-red"] + stats["dsfb-alt"]:.2%}\n'
            f'```\n'
        )

        return res


def get_finger(idx: int):
    fingermap = ['LP', 'LR', 'LM', 'LI', 'LI', 'RI', 'RI', 'RM', 'RR', 'RP']
    return fingermap[min(idx, 9)]


def shift(key: str):
    shifted = dict(zip(
        "abcdefghijklmnopqrstuvwxyz,./;'=[]",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ<>?:\"+{}"
    ))

    if key in shifted:
        return shifted[key]
    else:
        return key