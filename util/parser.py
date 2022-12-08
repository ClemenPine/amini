from typing import Tuple
from discord import Message

def get_arg(message: Message) -> str:
    args = message.content.split()
    return ' '.join(args[2:])


def get_args(message: Message) -> str:
    args = message.content.split()
    return args[2:]


def get_layout(message: Message) -> Tuple[str, str]:
    tokens = message.content.split('```')

    name = '-'.join(tokens[0].split()[2:]).lower()
    matrix = tokens[1].strip().lower()

    return name, matrix