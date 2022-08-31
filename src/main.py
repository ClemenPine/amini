import json
import bot

def main():
    with open('config.json', 'r') as f:
        token = json.load(f)['token']

    bot.init(token)


if __name__ == '__main__':
    main()