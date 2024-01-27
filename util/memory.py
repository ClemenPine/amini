import os
import json
import glob
from jellyfish import damerau_levenshtein_distance as lev

from util import authors
from util.consts import JSON
from admins import ADMINS

from core.keyboard import Layout, Position

def add(ll: Layout) -> bool:
    file = f'layouts/{ll.name.lower()}.json'

    if os.path.exists(file):
        return False

    with open(file, 'w') as f:
        f.write(json.dumps(vars(ll), indent=4, default=lambda o: o.__dict__))

    return True
    

def remove(name: str, *, id: int, admin: bool = False) -> bool:
    file = f'layouts/{name}.json'

    if not os.path.exists(file):
        return False

    with open(file, 'r') as f:
        data = json.load(f)

    check = (data['user'] == id) or admin

    if check:
        os.remove(file)

    return check


def get(name: str) -> Layout | None:
    file = f'layouts/{name}.json'

    if not os.path.exists(file):
        return None

    return parse_file(file)


def parse_file(file: str) -> Layout:
    with open(file, 'r') as f:
        data = json.load(f)

    keys = {
        k: Position(
            row=v["row"],
            col=v["col"],
            finger=v["finger"]
        ) for k, v in data["keys"].items()
    }

    ll = Layout(
        name=data["name"],
        user=data["user"],
        board=data["board"],
        keys=keys,
    )

    return ll

def find(name: str) -> Layout:
    file = f'layouts/{name}.json'

    if not os.path.exists(file):
        names = [x[8:-5] for x in glob.glob(f'layouts/*.json')]
        names = sorted(names, key=lambda x: len(x))

        closest = min(names, key=lambda x: lev((''.join(y for y in x.lower() if y in name)), name))

        file = f'layouts/{closest}.json'

    return parse_file(file)