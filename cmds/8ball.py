import random
from discord import Message

def exec(message: Message):
    return random.choice([
        'Yes', 'No', 'Count on it',
        'Maybe', 'Ask again', 'No doubt',
        'Absolutely', 'Cannot tell now', 
        'Very likely'
    ])