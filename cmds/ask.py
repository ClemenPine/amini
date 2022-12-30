import os
import json
import openai
from discord import Message

from util import parser

NAME = 'Amini'

HEADER = (
    f'The following is a conversation with a friend named {NAME}. '
    f'{NAME} is curious, empathetic, easy-going, and non-judgemental.'
)

def exec(message: Message):
    with open('openai.txt', 'r') as f:
        openai.api_key = f.read()

    channel = message.channel.id
    path = f'openai/{channel}.json'

    if os.path.exists(path):
        with open(path, 'r') as f:
            history = json.load(f)
    else:
        history = []

    input = parser.get_arg(message)

    history += [
        f'You: {input}',
        f'{NAME}:'
    ]

    prompt = '\n'.join([HEADER] + history[-10:])

    mod = openai.Moderation.create(prompt)
    if mod.results[0].flagged:
        return 'Sorry, openAI won\'t let me answer :('

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=200,
        prompt=prompt,
        stop=['You', f'{NAME}:']
    )

    res = completion.choices[0].text

    mod = openai.Moderation.create(res)
    if mod.results[0].flagged:
        return 'Sorry, openAI won\'t let me answer :('

    history[-1] += res

    with open(path, 'w') as f:
        f.write(json.dumps(history, indent=4))

    return res