import random
from discord import Message

RESTRICTED = False

def exec(message: Message):
    try:
        with open('scripts/ym.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines]

        if not lines:
            return "ym has no filling"

        random_line = random.choice(lines)

        return random_line

    except Exception as e:
        return f"An error occurred: {str(e)}"