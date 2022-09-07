import datetime
import discord

import parser, memory, speaker

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    args = message.content.split()
    
    id = message.author.id
    name = message.author.name
    date = str(datetime.date.today())

    if not args or args[0] not in ['!amini', '?amini', '!sudoamini', '?sudoamini']:
        return

    if args[0] in ['!sudoamini', '?sudoamini'] and id == 514971722626367517:
        id = 0

    if len(args) < 2:
        reply = speaker.hmm()
        await message.channel.send(reply, reference=message)
        return

    # parse args
    if args[1] == 'add':
        name = parser.get_name(message.content)
        matrix = parser.get_matrix(message.content)

        res, ll = memory.add(matrix, name=name, date=date, who=id)
        reply = speaker.added(res, layout=ll)

    elif args[1] == 'remove':
        name = parser.get_name(message.content)

        res = memory.forget(name, perm=id)
        reply = speaker.forgot(res, name=name)

    elif args[1] == 'rename':
        old, new = parser.get_names(message.content)

        res = memory.change(old, new, perm=id)
        reply = speaker.changed(res, old=old, new=new)

    elif args[1] == 'list':
        names = memory.recall(id)
        reply = speaker.recalled(names, who=name)

    elif args[1] == 'view':
        name = parser.get_name(message.content)

        ll = memory.find(name)
        reply = speaker.found(ll)

    elif args[1] == 'view-left':
        name = parser.get_name(message.content)

        ll = memory.find(name)
        ll.add('_', 'LT')

        reply = speaker.found(ll)

    elif args[1] == 'view-right':
        name = parser.get_name(message.content)

        ll = memory.find(name)
        ll.add('_', 'RT')

        reply = speaker.found(ll)

    elif args[1] == 'help':
        reply = speaker.help()

    else:
        reply = speaker.hmm(args[1])

    await message.channel.send(reply, reference=message)


def init(token: str):
    bot.run(token)