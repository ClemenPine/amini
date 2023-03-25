#!/usr/bin/env python

import glob
import logging
import discord
import datetime
from importlib import import_module

from cmds import help

CMINI_CHANNEL = 1063291226243207268

commands = [x.replace('/', '.')[5:-3] for x in glob.glob('cmds/*.py')]

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

logger = logging.getLogger('discord')

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message):
    args = message.content.split()

    if message.author.bot:
        return

    if not args or args[0] not in ['!amini', '!bmini', '!cmini']:
        return

    restricted = (
        message.channel.id != CMINI_CHANNEL and
        not isinstance(message.channel, discord.channel.DMChannel)
    )

    logger.info(f'{message.author.name}: {message.content}')

    command = args[1].lower()

    if len(args) < 2:
        reply = 'Try `!cmini help`'
    elif command in commands:
        mod = import_module(f'cmds.{command}')

        if not restricted or hasattr(mod, 'RESTRICTED') and not mod.RESTRICTED:
            reply = mod.exec(message)
        else:
            reply = f'please use this command in <#{CMINI_CHANNEL}> or in a dm'

    elif command == 'dm':
        channel = await bot.create_dm(message.author)
        await channel.send(help.exec(message))

        reply = f'Sent :)'
    else:
        reply = f'Error: {command} is not an available command'

    await message.channel.send(reply, reference=message)


def main():
    date = datetime.datetime.now()

    with open('token.txt', 'r') as f:
        token = f.read()

    bot.run(token)


if __name__ == '__main__':
    main()
