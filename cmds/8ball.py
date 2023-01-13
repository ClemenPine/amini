import random
from discord import Message

RESTRICTED = False

def exec(message: Message):
    return random.choice([
        'Yes', 'No', 'Count on it',
        'Maybe', 'No doubt',
        'Absolutely', 'Very likely'
    ])