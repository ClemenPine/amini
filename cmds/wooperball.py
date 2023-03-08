import random
from discord import Message

RESTRICTED = False

def exec(message: Message):
    return random.choice([
        '<:wooper:1081033714043207771>'
    ])
