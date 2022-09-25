import re
import json 

languages = [
    "english",
    "english_1k",
    "english_5k",
    "english_10k",
    "english_450k",
]

def load_language(lang: str='english'):
    file = f'languages/{lang}.json'
    
    with open(file, 'r') as f:
        return json.load(f)

def find(string: str, *, file: str='corpora/mt-quotes.txt'):
    with open(file, 'r') as f:
        text = f.read().replace('\n', ' ')

    count = len(re.findall(string, text))
    if count:
        res = len(text) // count
    else:
        res = 0

    return res