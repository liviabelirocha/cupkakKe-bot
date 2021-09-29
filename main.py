import discord
from discord.ext import commands

from settings import *

import Music

cogs = [Music]

intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(DISCORD_PRIVATE_KEY)