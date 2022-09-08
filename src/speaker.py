import json
import random
from typing import List

import kb

replies = json.load(open('src/static/responses.json'))

def added(res: str, *, layout: kb.Layout):
    print(f'added: {layout.name}, {res}')

    if res == 'OK':
        reply = random.choice(replies['add'])
        return reply.replace('NAME', layout.name) + str(layout)

    elif res == 'LENGTH':
        return random.choice(replies['length'])

    elif res == 'NAME':
        reply = random.choice(replies['name-taken'])
        return reply.replace('NAME', layout.name)

    elif res == 'MATRIX':
        return random.choice(replies['layout-taken'])


def forgot(res: str, *, name: str):
    print(f'removed: {name}, {res}')

    if res == 'OK':
        reply = random.choice(replies['remove'])
        return reply.replace('NAME', name)

    elif res == 'NOPERM':
        return random.choice(replies['noperm-remove'])

    elif res == 'NOLAYOUT':
        reply = random.choice(replies['null-layout'])
        return reply.replace('NAME', name)


def changed(res: str, *, old: str, new: str):
    print(f'renamed: {old} -> {new}, {res}')
    
    if res == 'OK':
        reply = random.choice(replies['change'])

        reply = reply.replace('OLD', old)
        reply = reply.replace('NEW', new)

        return reply
    
    elif res == 'TAKEN':
        reply = random.choice(replies['name-taken'])
        return reply.replace('NAME', new)

    elif res == 'NOPERM':
        return random.choice(replies['noperm-rename'])

    elif res == 'NOLAYOUT':
        reply = random.choice(replies['null-layout'])
        return reply.replace('NAME', old)


def recalled(names: str, *, who: str):
    print(f'list: {len(names.split())}')
    
    if names:
        return f'```{who}\'s layouts:\n{names}\n```'
    else:
        return random.choice(replies['no-layouts?'])


def found(ll: kb.Layout):
    print(f'found: {ll.name}')
    return str(ll)


def named(names: List[str]):
    print(f'named: {names[:5]}')
    if not names:
        return random.choice(replies['stumped'])

    else:
        names = '\n'.join(x for x in names[:10])
        reply = (
            f'{random.choice(replies["name"])}\n'
            f'```\n'
            f'{names}\n'
            f'```\n'
        )

        return reply


def hmm(arg: str=''):
    print(f'unknown: {arg}')

    if arg:
        reply = random.choice(replies['unknown'])
        return reply.replace('ARG', arg)
    else:
        return 'Try `!amini help`'

def help():
    print(f'help')

    return (
        f'```\n'
        f'Usage: !amini [command]\n'
        f'\n'
        f'view [layout]\n'
        f'  - see the stats of a layout\n'
        f'  - view-left [layout]\n'
        f'      - force left thumb use for space\n'
        f'  - view-right [layout]\n'
        f'      - force right thumb use for space\n'
        f'list\n'
        f'  - see a list of your layouts\n'
        f'\n'
        f'add [name] [layout]\n'
        f'  - contribute a new layout\n'
        f'remove [name]\n'
        f'  - delete one of your layouts\n'
        f'rename [old_name] [new_name]\n'
        f'  - change one of your layout\'s name\n'
        f'names [layout]\n'
        f'  - suggest some names for a layout\n'        
        f'```'
    )
    