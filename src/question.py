import json
import requests

def get():
    file = 'https://story-shack-cdn-v2.glitch.me/generators/random-question-generator'

    req = requests.get(file)
    res = json.loads(req.text)

    return res['data']['name']