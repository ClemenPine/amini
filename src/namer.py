import json
import jellyfish as jf

def get_table():
    table = {}

    with open('src/static/freq.json', 'r') as f:
        words = json.load(f)

    for word, freq in words.items():
        code = jf.match_rating_codex(word)

        if not code in table:
            table[code] = {}

        table[code][word] = freq

    return table


def get_names(matrix: str):
    table = get_table()
    layout = matrix.split('\n')
    
    res = {}
    for row in layout:
        string = ''.join(row.split())

        for i in range(len(string) - 3):
            substr = string[i:i+4]
            code = jf.match_rating_codex(substr)

            if code in table:
                words = {k: v for k, v in table[code].items() if all(y in k for y in substr)}

                if words:
                    res |= words

    res = sorted(res.keys(), key=lambda x: int(res[x]), reverse=True)
    return list(res)