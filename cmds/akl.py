import discord.utils
from discord import Client, Guild

AKL_ID = 807843650717483049

LAYOUT_ROLES: list[str] = [
    'CTGAP',
    'Workman',
    'Taipo',
    'TypeHack',
    'SIND',
    'Steno',
    'Sertain',
    'Semimak',
    'RSTHD',
    'RSI Terminated',
    'QWERTY',
    'QGMLWY',
    'Other (self-made)',
    'Other',
    'Nerps',
    'Neo',
    'MTGAP',
    'MessagEase',
    'ISRT',
    'Halmak',
    'Hands Down',
    'FR-Godox',
    'Engram',
    'Dvorak',
    'Colemak Qi',
    'ColemaQ',
    'Colemak DHv',
    'Colemak DH',
    'Colemak',
    'boo'
    'BÉPO',
    'BEAKL',
    'ASETNIOP',
    'APT',
    'Canary',
    'Sturdy',
    'Nrts Haei',
]

def exec(bot: Client):
    guild: Guild = bot.get_guild(AKL_ID)
    if not guild:
        return 'Error: Cannot find akl server'

    role_counts: dict[str, int] = {}
    for role_name in LAYOUT_ROLES:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            role_counts[role_name] = len(role.members)

    sorted_role_counts: list[tuple[str, int]] = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_role_counts = sorted_role_counts[:20]

    res = ['```',
           '--- AKL STATS ---',
           'Most used layouts:']
    res.extend(f'    {role_name:<15} ({count} users)' for (role_name, count) in sorted_role_counts)
    res.append('```')
    return '\n'.join(res)
