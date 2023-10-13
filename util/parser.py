from typing import Tuple
from discord import Message
from util.consts import TRIGGERS
from typing import Type

def get_arg(message: Message) -> str:
    args = message.content.split()

    return ' '.join(args[2:] if args[0] in TRIGGERS else args[1:])


def get_args(message: Message) -> list[str]:
    args = message.content.split()
    return args[2:] if args[0] in TRIGGERS else args[1:]


def get_layout(message: Message) -> Tuple[str, str]:
    tokens = message.content.split('```')

    args = tokens[0].split()
    name = '-'.join(args[2:] if args[0] in TRIGGERS else args[1:]).lower()
    matrix = tokens[1].strip().lower()

    return name, matrix

def get_kwargs(message: Message,
               arg_type: Type[str | list[str]],
               **cmd_kwargs: Type[bool | list]) -> dict[str, str | bool | list[str]]:
    """
    - message: user's message list[str]
    - arg type: str or list[str]
    - kwargs: arguments with `--` prefix
    - example:
        `get_kwargs(Message, min=bool, max=bool)`
    - return:
        `dict {'args': str or list[str], 'kwarg1': Any, 'kwarg2': ...}`
    """
    message_as_list = message.content.split()
    command: list[str] = message_as_list[2:] if message_as_list[0] in TRIGGERS else message_as_list[1:]

    if not command:
        if arg_type == list[str]:
            return {'args': ['']}
        else:
            return {'args': ''}

    if 'args' in cmd_kwargs:
        cmd_kwargs.pop('args')  # reserved, no 'args' in kwargs

    args: str | list[str] = ''
    if command[0].startswith('--'):
        args = command[0]
        command.pop(0)

    # ensure all positional
    kwargs_start_index = 0
    for i, word in enumerate(command):
        if word.startswith('--') and word.removeprefix('--') in cmd_kwargs:
            kwargs_start_index = i
            break
        args += ' ' + word
    args = args.strip()
    if arg_type == list[str]:
        args = args.split()

    # make default dict
    parsed_kwargs = {'args': args}
    for kw_name, kw_type in cmd_kwargs.items():
        if kw_type == bool:
            default = False
        elif kw_type == list:
            default = []
        else:
            default = None
        parsed_kwargs[kw_name] = default

    # handle keyword
    temp_list = []
    prev_word = ''
    in_list = False
    for word in command[kwargs_start_index:]:
        if word.removeprefix('--') not in cmd_kwargs:
            if in_list:
                temp_list.append(word)
            continue

        word = word.removeprefix('--')
        kw_type = cmd_kwargs.get(word, None)
        if in_list and kw_type is not None:  # encountered next keyword
            parsed_kwargs[prev_word] = temp_list.copy()
            temp_list.clear()
            in_list = False
        if kw_type == bool:
            parsed_kwargs[word] = True
        if kw_type == list:
            in_list = True
            prev_word = word

    if in_list:
        parsed_kwargs[prev_word] = temp_list

    return parsed_kwargs
