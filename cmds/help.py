import os
from discord import Message
from importlib import import_module
from more_itertools import windowed

WIDTH = 6
INDENT = '    '

def exec(message: Message):
    lines = ['Usage: `!cmini (command) [args]`']
    lines.append('```')

    with os.scandir('cmds') as it:
        entries = sorted(
            [entry for entry in it
            if not entry.is_symlink() and
            entry.name.endswith('.py')],
        key=lambda x:x.name)

    for entry in entries:
        file = entry.name
        mod = import_module(f'cmds.{file[:-3]}')

        if all(hasattr(mod, func) for func in ['exec', 'desc', 'use']):
            use = mod.use()
            desc = mod.desc().split()

            lines.append(use)
            lines += [
                INDENT + ' '.join(x) for x in windowed(
                    desc, n=WIDTH, step=WIDTH, fillvalue=''
                )
            ]

    lines.append('```')

    return '\n'.join(lines)