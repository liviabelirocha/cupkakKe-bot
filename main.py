import discord
from discord.ext import commands

from settings import *

import Music

cogs = [Music]

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

for cog in cogs:
    cog.setup(client)

client.run(DISCORD_PRIVATE_KEY)
