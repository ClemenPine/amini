import argparse

from discord import Message
from importlib import import_module

from util import layout, memory, parser
from util.consts import JSON

RESTRICTED = False

def exec(message: Message):
    command = parser.get_arg(message)

    if not command:
        kw_tips = ['Usage: `mod layout_name [--kwarg1, --kwarg2, ...]`', '```']
        kw_tips.extend(f'--{kw}:\n    {__get_layout_desc(kw)}' for kw in __Parser.keywords.keys() if kw != 'swap')
        kw_tips.extend(['--swap:\n    alias of --cycle', '```'])
        return '\n'.join(kw_tips)
    kwargs = __Parser.get_kwargs(command)

    ll = memory.find(kwargs['layout_name'].lower())

    if not ll:
        return f'Error: could not find layout `{kwargs["layout_name"]}`'
    
    if kwargs['angle'] and kwargs['unangle']:
        kwargs['angle'] = False  # `--angle --unangle` defaults to unanglemodded

    kwargs['cycle'].extend(kwargs['swap'])  # combine cycle with swap alias

    try:
        if kwargs['angle']:
            __modify_layout(ll, 'angle')
        if kwargs['unangle']:
            __modify_layout(ll, 'unangle')
        if kwargs['mirror']:
            __modify_layout(ll, 'mirror')
        if kwargs['cycle']:
            __modify_layout(ll, 'cycle', kwargs['cycle'])
    except ValueError as e:
        return str(e)

    ll['name'] += ' (modified)'

    return layout.to_string(ll, id=message.author.id)

def use():
    return 'mod [name] [--kwargs]'

def desc():
    return 'see the stats of a layout with chained modifications'

def __modify_layout(ll: JSON, mode: str, *args):
    mod = import_module(f'cmds.{mode}')
    mod.modify(ll, *args)

def __get_layout_desc(mode: str) -> str:
    mod = import_module(f'cmds.{mode}')
    return mod.desc()

class __Parser:
    keywords: dict[str, dict] = {
        'angle': {'action': 'store_true'},
        'unangle': {'action': 'store_true'},
        'mirror': {'action': 'store_true'},
        'cycle': {'nargs': '*', 'default': None},
        'swap': {'nargs': '*', 'default': None}
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('layout_name', nargs='*')
    for keyword, arg_config in keywords.items():
        parser.add_argument(f'--{keyword}', **arg_config)

    @classmethod
    def get_kwargs(cls, command: str) -> dict[str, str | bool | list[str]]:
        command: list[str] = command.split()
        kwargs, unknown_args = cls.parser.parse_known_args(command)
        kwargs.layout_name = " ".join(kwargs.layout_name)
        if kwargs.cycle is None:
            kwargs.cycle = []
        if kwargs.swap is None:
            kwargs.swap = []
        return vars(kwargs)

