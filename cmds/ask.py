import openai
from discord import Message

from util import parser

def exec(message: Message):
    with open('openai.txt', 'r') as f:
        openai.api_key = f.read()

    prompt = parser.get_arg(message)

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=50,
        prompt=prompt
    )

    return completion.choices[0].text