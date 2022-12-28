import json
from discord import Message

from util import memory, parser

def exec(message: Message):
    name = parser.get_arg(message)
    id = message.author.id

    ll = memory.find(name)

    with open('likes.json', 'r') as f:
        likes = json.load(f)

    if not ll['name'] in likes:
        likes[ll['name']] = []

    if not id in likes[ll['name']]:
        likes[ll['name']].append(id)
        action = 'liked'
    else:
        likes[ll['name']].remove(id)
        action = 'unliked'

    with open('likes.json', 'w') as f:
        f.write(json.dumps(likes, indent=4))


    return f'You {action} {ll["name"]}. (Now at {len(likes[ll["name"]])} likes)'