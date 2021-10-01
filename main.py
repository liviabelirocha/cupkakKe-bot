import discord
from discord.ext import commands
from decouple import config

from web_server import keep_alive

import Music

cogs = [Music]

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

for cog in cogs:
    cog.setup(client)

keep_alive()

client.run(config("DISCORD_PRIVATE_KEY"))
