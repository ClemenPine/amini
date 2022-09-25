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