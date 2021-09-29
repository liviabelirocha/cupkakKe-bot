import re

import discord
from discord.ext import commands
import youtube_dl

from settings import *

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You have to be in a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None: 
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query):
        await self.join(ctx)

        ctx.voice_client.stop()

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            if not re.match(URL_REGEX, query):
                url = await self.handle_search_name(ydl, query)
            else:
                url = await self.handle_url(ydl, query)
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Audio paused")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Audio resumed")

    async def handle_url(self, ydl, url):
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        return url2

    async def handle_search_name(self, ydl, name):
        info = ydl.extract_info(f"ytsearch:{name}", download=False)
        url = info['entries'][0]['formats'][0]['url']
        return url


def setup(client):
    client.add_cog(Music(client))