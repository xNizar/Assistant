import datetime

import aiohttp

import discord
from discord.ext import commands

from cogs.utils.embed import EmbedUtils


class Dadjoke:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"}) as r:
                res = await r.json()
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color())
        embed.add_field(name="Dad Joke \U0001f935", value=f'```fix\n{res["joke"]}```')
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Dadjoke(bot))