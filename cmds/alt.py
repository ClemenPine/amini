import operator

from typing import Dict, List, Tuple
from itertools import product, pairwise

from discord import Message
from util import parser, authors, memory
from admins import ADMINS

RESTRICTED = False

class FingerMap:
    def __init__(self, fmap: List[List[str]]):
        self.fmap = fmap

    def __getitem__(self, index: Tuple[int, int]) -> str:
        row, col = index
        return self.fmap[row][col]

def parse(word: str, layout: Dict[str, Tuple], fingermap: FingerMap) -> List[str]:
    options = [fingermap[layout[char]] for char in word]
    columns = [layout[char][1] for char in word]
    wpairs = list(pairwise(word))

    f = lambda x: "prmitTIMRPP".index(x)
    eq = lambda x: operator.eq(*x[0]) and not operator.eq(*x[1])
    dist = lambda x, y: abs(f(x) - y)

    def score(option: List[str]) -> Tuple[int, int, int]:
        opairs = list(pairwise(option))
        sfb_score = sum(map(eq, zip(opairs, wpairs)))
        sfs_score = len(set(zip(option, word)))
        dfh_score = sum([dist(*cxy) for cxy in zip(option, columns)])
        return sfb_score, sfs_score, dfh_score

    predictions = sorted([(option, score(option))
        for option in product(*options)
        ], key=lambda k: (k[1][0], k[1][1], k[1][2])
    )

    return predictions[0]

def exec(message: Message):
    user = message.author.id
    user_name = authors.get_name(user).lower()
    # Check current user
    # if user_name not in ADMINS:
        # return 'Unauthorized'

    args = parser.get_args(message)

    if len(args) < 2:
        return "Usage: alt <layout> <word>"
    
    name, word = args
    ll = memory.find(name.lower())
    if not ll:
        return f"Could not find layout: {name}"

    layout = {
        k:(v["row"],v["col"])
        for k, v in ll["keys"].items()
    }

    fingermap = FingerMap([
        # q   w    e    r    t    y    u    i    o    p    [   ]   \
        ["p","rp","mr","im","i","IM","IM","MIR","RM","RP","P","P","P"],
        # a   s    d    f    g   h    j    k    l   ;   '
        ["p","rm","mi","im","i","IM","IM","MR","R","P","P"],
        # z   x    c    v   b    n    m    ,    .   /
        ["r","mr","im","im","Ii","IM","IM","MR","R","P"],
        # thumb alpha
        ["T"]
    ])

    fingernames = dict(zip(
        "prmitTIMRP", [f"L{f}" for f in "PRMIT"] + [f"R{f}" for f in "TIMRP"]
    ))

    # Filter characters from word that aren't in layout
    word = ''.join(filter(lambda c: c in layout, word.lower()))
    if len(word) > 15:
        return "Max word length: 15"

    alts, scores = parse(word, layout, fingermap)
    sfb, use, dfh = scores

    return '```' + f"Alt fingering suggestion for '{word}' ({name})\n" + \
        ' '.join([fingernames[o] for o in alts]) + "\n" + \
        ''.join([f"{c:3}" for c in word]) + "\n" + \
        ' '.join([fingernames[fingermap[layout[c]][0]] for c in word]) + " (traditional)\n" + \
        f"SFB: {sfb} / {sfb/len(word):.2%}\n" \
        f"USE: {use} / {use/len(word):.2%}\n" \
        f"DFH: {dfh} / {dfh/len(word):.2%}" \
    + '```'
