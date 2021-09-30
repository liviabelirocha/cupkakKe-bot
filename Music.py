import re

import discord
from discord.ext import commands
import youtube_dl

from settings import *


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False
        self.queue = []

        self.vc = ""

    def handle_url(self, ydl, url):
        try:
            info = ydl.extract_info(url, download=False)
            return {"url": info["formats"][0]["url"], "title": info["title"]}
        except Exception:
            return False

    def handle_search_name(self, ydl, name):
        try:
            info = ydl.extract_info(f"ytsearch:{name}", download=False)["entries"][0]
            return {"url": info["formats"][0]["url"], "title": info["title"]}
        except Exception:
            return False

    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True

            url = self.queue[0]["url"]
            self.queue.pop(0)

            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            self.vc.play(source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You have to be in a voice channel.")
            return False

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        return True

    @commands.command()
    async def leave(self, ctx):
        self.queue.clear()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query):
        joined = await self.join(ctx)

        if not joined:
            return

        self.vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            if not re.match(URL_REGEX, query):
                song = self.handle_search_name(ydl, query)
            else:
                song = self.handle_url(ydl, query)

            if not song:
                await ctx.send("An error has occurred. Could not find song.")
                return

            await ctx.send(f"{song['title']} added to queue")
            self.queue.append(song)

            if not self.is_playing:
                self.play_next()

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Audio paused")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Audio resumed")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            self.play_next()


def setup(client):
    client.add_cog(Music(client))
