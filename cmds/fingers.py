import json

from discord import Message
from util import analyzer, authors, corpora, layout, memory, parser
from util.consts import JSON

from typing import Final

RESTRICTED = False

LEFT_HAND = ['LI', 'LM', 'LR', 'LP']
RIGHT_HAND = ['RI', 'RM', 'RR', 'RP']
THUMBS = ['LT', 'RT', 'TB']
FINGERS = LEFT_HAND + RIGHT_HAND + THUMBS
TABLE: JSON = analyzer.get_table()

class Fingers(dict[str, float]):
    def __iadd__(self, other: dict[str, float]):
        for finger in self:
            self[finger] += other[finger]
        return self

    def __itruediv__(self, other_or_num: dict[str, float] | int | float):
        if isinstance(other_or_num, int | float):
            # Divide all by a constant
            for finger in self:
                self[finger] /= other_or_num
        else:
            # Element wise division
            for finger in self:
                self[finger] /= other_or_num[finger]
        return self

class GetFingerStats:
    __slots__ = ("__stats", "__operator")

    def __init__(self, *stats: str, operator='+'):
        self.__stats: Final[tuple[str]] = stats
        self.__operator: Final[str] = operator

    def __call__(self, ll: JSON, trigrams: JSON) -> Fingers[str, float]:
        # Get the first stat
        fingers_usage: Fingers[str, float] = self.get_fingers_usage(ll, trigrams, stat=self.__stats[0])

        # Gets only 1 stat
        if len(self.__stats) == 1:
            return fingers_usage

        # Ratio of two stats: stat[0] / stat[1]
        if self.__operator == '/':
            fingers_usage /= self.get_fingers_usage(ll, trigrams, stat=self.__stats[1])
            return fingers_usage

        # Other: sum of all stats
        for stat in self.__stats[1:]:
            fingers_usage += self.get_fingers_usage(ll, trigrams, stat=stat)
        return fingers_usage

    @staticmethod
    def get_fingers_usage(ll: JSON, trigrams: JSON, *, stat: str) -> Fingers[str, float]:
        fingers_usage: Fingers[str, float] = Fingers.fromkeys(FINGERS, 0)  # NoQA: `fromkeys` returns `Fingers`
        get_usage = stat == 'usage'
        get_sfb = stat == 'sfb'
        get_sfr = stat == 'sfr'

        total = 0

        for trigram, freq in trigrams.items():
            if ' ' in trigram:
                continue

            fingers = [ll['keys'][x]['finger'] for x in trigram.lower() if x in ll['keys']]

            if get_usage:
                for finger in fingers:
                    fingers_usage[finger] += freq / len(fingers)
                if fingers:
                    total += freq  # Ignore unused keys

            else:
                trigram_type = get_trigram_type(fingers, trigram)
                if trigram_type == stat:
                    for finger in fingers:
                        fingers_usage[finger] += freq / len(fingers)

                # Sfr: ignore unknown sfr
                # actual sfr (util.analyzer.trigrams() -> {}['sfR'] includes unknowns)
                if not get_sfr or get_sfr and fingers:
                    total += freq

        fingers_usage /= total

        if get_sfb:
            fingers_usage /= 2

        return fingers_usage


def is_sfr(trigram: str) -> bool:
    return trigram[0] == trigram[1] or trigram[1] == trigram[2] or trigram[0] == trigram[2]

def get_trigram_type(fingers: list[str], trigram: str) -> str:
    key = '-'.join(fingers)
    key = key.replace('TB', 'RT')
    if is_sfr(trigram):
        gram_type = 'sfR'
    elif key in TABLE:
        gram_type = TABLE[key]
    else:
        gram_type = 'unknown'
    return gram_type


STATS: Final[dict[str, GetFingerStats]] = {
    'usage': GetFingerStats('usage'),
    'alt': GetFingerStats('alternate'),
    'sfb': GetFingerStats('sfb'),
    'sfs': GetFingerStats('dsfb', 'dsfb-red', 'dsfb-alt', operator='+'),
    'sfr': GetFingerStats('sfR'),
    'red': GetFingerStats('redirect'),
    'oneh': GetFingerStats('oneh-in', 'oneh-out', operator='+'),
    'inroll': GetFingerStats('roll-in'),
    'outroll': GetFingerStats('roll-out'),
    'roll': GetFingerStats('roll-in', 'roll-out', operator='+'),
    'inrollratio': GetFingerStats('roll-in', 'roll-out', operator='/'),
    'outrollratio': GetFingerStats('roll-out', 'roll-in', operator='/'),
    'inrolltal': GetFingerStats('roll-in', 'oneh-in', operator='+'),
    'outrolltal': GetFingerStats('roll-out', 'oneh-out', operator='+'),
    'rolltal': GetFingerStats('roll-in', 'oneh-in', 'roll-out', 'oneh-out', operator='+')
}

STATS_ALIAS: Final[dict[str, str]] = {
    '': 'usage',
    'alts': 'alt', 'alternate': 'alt',
    'sfbs': 'sfb',
    'dsfb': 'sfs', 'dsfbs': 'sfs',
    # (sfr: no aliases)
    'redirect': 'red', 'redirects': 'red',
    'onehand': 'oneh', 'onehands': 'oneh',
    'inrolls': 'inroll', 'roll-in': 'inroll',
    'outrolls': 'outroll', 'roll-out': 'outroll',
    'rolls': 'roll', 'roll-total': 'roll',
    'roll-in-ratio': 'inrollratio',
    'roll-out-ratio': 'outrollratio',
    'inrolltals': 'inrolltal',
    'outrolltals': 'outrolltal',
    'rolltals': 'rolltal', 'rolltotal': 'rolltal'
}

def exec(message: Message):
    user = message.author.id
    trigrams: JSON = corpora.ngrams(3, id=user)
    args = [item.lower() for item in parser.get_args(message)]

    if len(args) == 0:
        return f'```\nSupported rank stats:\n{" ".join(STATS)}```'

    name = args[0] if len(args) > 0 else ''
    stat = args[1] if len(args) > 1 else ''
    ll = memory.find(name.lower())

    corpus: str = corpora.get_corpus(id=user)
    author: str = authors.get_name(ll['user'])

    if not ll:
        return f'Error: could not find layout `{name}`'

    get_finger_stats = STATS.get(stat, None)

    if get_finger_stats is None:
        stat = STATS_ALIAS.get(stat, None)
        get_finger_stats = STATS.get(stat, None)

    if get_finger_stats is None:
        return f'Error: {stat} not supported'

    finger_stats = get_finger_stats(ll, trigrams)

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

    output = [f'```\n{ll["name"]} ({stat}) ({author}) ({likes} {like_string})',
              layout.get_matrix_str(ll),
              f'\n{corpus.upper()}:']

    for lfinger, rfinger in zip(LEFT_HAND, RIGHT_HAND):
        lfreq = finger_stats[lfinger]
        rfreq = finger_stats[rfinger]
        output.append(f'  {lfinger}: {lfreq:>6.2%}    {rfinger}: {rfreq:>6.2%}')
    output.append('')

    used_thumb = False
    for finger in THUMBS:
        freq = finger_stats[finger]
        if freq == 0:
            continue
        output.append(f'  {finger}: {freq:.2%}')
        used_thumb = True

    if used_thumb:
        output.append('')
    output.append(f'  Total: {sum(finger_stats.values()):.2%}')

    output.append('```')

    return '\n'.join(output)

def use():
    return 'fingers [layout] [metric]'

def desc():
    return 'view stats of each finger'
