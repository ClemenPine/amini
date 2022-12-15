import openai
from discord import Message

from util import parser

def exec(message: Message):

    with open('openai.txt', 'r') as f:
        openai.api_key = f.read()

    prompt = parser.get_arg(message)

    if prompt[-1] != '?':
        prompt += '?'

    mod = openai.Moderation.create(prompt)
    if mod.results[0].flagged:
        return 'Sorry, openAI won\'t let me answer :('

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=200,
        prompt=prompt
    )

    res = completion.choices[0].text

    mod = openai.Moderation.create(res)
    if mod.results[0].flagged:
        return 'Sorry, openAI won\'t let me answer :('

    return res