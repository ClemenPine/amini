import json
from discord import Message

def update(message: Message):
    with open('authors.json', 'r') as f:
        authors = json.load(f)

    user = message.author.name
    id = message.author.id

    authors[user] = id

    with open('authors.json', 'w') as f:
        f.write(json.dumps(authors, indent=4))


def get_id(name: str) -> int:
    with open('authors.json', 'r') as f:
        authors = json.load(f)

    if name in authors:
        return int(authors[name])
    else:
        return 0


def get_name(id: int) -> str:
    with open('authors.json', 'r') as f:
        authors = json.load(f)

    names = [k for k, v in authors.items() if int(v) == id]

    if names:
        return names[0]
    else:
        return 'unknown'