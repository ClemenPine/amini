from typing import List

import kb

def added(res: str, *, layout: kb.Layout):
    print(f'added: {layout.name}, {res}')

    if res == 'OK':
        return (
            f'I\'ve successfully added {layout.name} to my servers\n'
            f'{str(layout)}'
        )

    elif res == 'NAME':
        return f'"{layout.name}" has been reserved by an existing layout on my servers'

    elif res == 'MATRIX':
        return f'This layout already exists on my servers'


def forgot(res: str, *, name: str):
    print(f'removed: {name}, {res}')

    if res == 'OK':
        return f'I\'ve successfully removed {name} from my servers'

    elif res == 'NOPERM':
        return f'I cannot remove a layout that you don\'t own'

    elif res == 'NOLAYOUT':
        return f'I couldn\'t find "{name}" in my servers'


def changed(res: str, *, old: str, new: str):
    print(f'renamed: {old} -> {new}, {res}')
    
    if res == 'OK':
        return f'I\'ve successfully renamed {old} to "{new}"'
    
    elif res == 'TAKEN':
        return f'The name "{new}" is already in use'

    elif res == 'NOPERM':
        return f'I cannot rename a layout that you don\'t own'

    elif res == 'NOLAYOUT':
        return f'I couldn\'t find "{old}" in my servers'


def recalled(names: str, *, who: str):
    print(f'list: {len(names.split())}')
    
    if names:
        return f'```{who}\'s layouts:\n{names}\n```'
    else:
        return 'It seems like you haven\'t added any layouts yet...'


def found(ll: kb.Layout):
    print(f'found: {ll.name}')
    return str(ll)


def hmm(arg: str=''):
    print(f'unknown: {arg}')

    if arg:
        return f'I\'m not really sure what "{arg}" means'
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
        f'list\n'
        f'  - see a list of your layouts\n'
        f'\n'
        f'add [name] [layout]\n'
        f'  - contribute a new layout\n'
        f'remove [name]\n'
        f'  - delete one of your layouts\n'
        f'rename [old_name] [new_name]\n'
        f'  - change one of your layout\'s name\n'
        f'```'
    )