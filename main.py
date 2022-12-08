import glob
import discord
from importlib import import_module

from cmds import help

commands = [x.replace('/', '.')[5:-3] for x in glob.glob('cmds/*.py')]

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_message(message: discord.Message):
    args = message.content.split()

    if not args or args[0] != '!amini':
        return
    
    command = args[1].lower()

    if len(args) < 2:
        reply = 'Try `!amini help`'
    elif command in commands:
        mod = import_module(f'cmds.{command}')
        reply = mod.exec(message)
    elif command == 'dm':
        channel = await bot.create_dm(message.author)
        await channel.send(help.exec(message))

        reply = f'Sent :)'
    else:
        reply = f'Error: {command} is not an available command'

    await message.channel.send(reply, reference=message)


def main():
    with open('token.txt', 'r') as f:
        token = f.read()

    bot.run(token)


if __name__ == '__main__':
    main()