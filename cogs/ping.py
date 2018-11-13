import datetime
import random

import discord
from discord.ext import commands

from cogs.utils.embed import EmbedUtils


class Miscellanous:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                              description='Pinging...')
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        t = await ctx.send(embed=embed)
        ms = t.created_at - datetime.datetime.utcnow()
        embed1 = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                               description=f'Pong! `{str(ms)[-2:]}`ms')
        embed1.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await t.edit(embed=embed1)


def setup(bot):
    bot.add_cog(Miscellanous(bot))