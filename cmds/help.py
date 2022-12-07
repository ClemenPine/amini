import glob
from discord import Message
from importlib import import_module
from more_itertools import windowed

WIDTH = 6
INDENT = '    '

def exec(message: Message):
    lines = ['Usage: `!amini (command) [args]`']
    lines.append('```')

    for file in sorted(glob.glob('cmds/*.py')):
        mod = import_module(f'cmds.{file[5:-3]}')
        
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

def use():
    return 'help'

def desc():
    return 'display this help page'