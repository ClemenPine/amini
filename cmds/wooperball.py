import random
from discord import Message

RESTRICTED = False

def exec(message: Message):
    return random.choice([
        '<a:wooperno:1085582045121613874>',
        '<a:wooper:1081033714043207771>'
    ])
