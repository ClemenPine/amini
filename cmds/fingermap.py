import json

from discord import Message
from util import layout, memory, parser, authors
from core.keyboard import Layout

RESTRICTED = False

def exec(message: Message):
    name = parser.get_arg(message)
    ll = memory.find(name.lower())
    return to_string(ll)

def use():
    return 'fingermap [layout_name]'

def desc():
    return 'view the fingermap of a layout'

def to_string(ll: Layout):
    author: str = authors.get_name(ll.user)
    
    with open('likes.json', 'r') as f:
        likes = json.load(f)

    if ll.name in likes:
        likes = len(likes[ll.name])
    else:
        likes = 0

    if likes == 1:
        like_string = 'like'
    else:
        like_string = 'likes'
    
    res = (
        f'```\n'
        f'{ll.name} ({author}) ({likes} {like_string})',
        f'{layout.get_matrix_str(ll)}\n', 
        f'{layout.get_fingermatrix_str(ll)}\n', 
        f'```'
    )

    return '\n'.join(res)