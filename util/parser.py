from typing import Tuple
from discord import Message
from util.consts import TRIGGERS

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