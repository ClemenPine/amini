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
    # Get list of finger options for each character
    options = [fingermap[layout[char]] for char in word]
    # Store list of character pairs in word
    wpairs = list(pairwise(word))

    # Check if same finger (SFB) and different key (!SFR)
    eq = lambda x: operator.eq(*x[0]) and not operator.eq(*x[1])

    # Walk cartesian product of finger options
    for option in product(*options):
        # Get finger pairs for this option
        opairs = list(pairwise(option))
        # Get SFB count
        sfbs = sum(map(eq, zip(opairs, wpairs)))
        # Else return the first 0 SFB option
        if sfbs == 0:
            return option, sfbs

    # Return first prediction worst case
    option = next(product(*options))
    return option, sum(map(eq, zip(list(pairwise(option)), wpairs)))

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
        ["p","rp","mr","im","im","IM","IM","MIR","RM","RP","P","P","P"],
        # a   s    d    f    g   h    j    k    l   ;   '
        ["p","rm","mi","im","i","IM","IM","MR","R","P","P"],
        # z   x    c    v   b    n   m    ,    .   /
        ["r","mr","mi","i","Ii","I","IM","MR","R","P"],
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

    alts, sfbs = parse(word, layout, fingermap)

    return '```' + f"Alt fingering suggestion for '{word}' ({name})\n" + \
        ' '.join([fingernames[fingermap[layout[c]]] for c in word]) + " (traditional)\n" + \
        ''.join([f"{c:3}" for c in word]) + "\n" + \
        ' '.join([fingernames[o] for o in alts]) + "\n" + \
        f"SFBs: {sfbs} / {sfbs/len(word):.2%}" \
    + '```'
