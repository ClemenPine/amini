from discord import Message

from util import layout, memory, parser

def exec(message: Message):
    args = parser.get_args(message)

    ll = memory.find(args[0])
    if not ll:
        return f'Error: couldn\'t find any layout named `{args[0]}`'

    for cycle in args[1:]:
        cmap = dict(zip(cycle, cycle[1:] + cycle[0]))
        keymap = {k: ll['keys'][k] for k in cycle}

        for key, val in cmap.items():
            ll['keys'][key] = keymap[val]  

    ll['name'] += ' (modified)'

    return layout.to_string(ll)

def use():
    return 'cycle [layout_name] [chars]'

def desc():
    return 'cycle a layout\'s letters around'