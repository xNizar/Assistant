import datetime

import discord
from discord.ext import commands
import aiohttp

from cogs.utils.embed import EmbedUtils


class Emojis:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ue', 'uemoji'])
    @commands.has_permissions(manage_emojis=True)
    async def uploademoji(self, ctx, url: str, name: str):
        response = aiohttp.ClientSession().get(url).read()
        emoji = await ctx.guild.create_custom_emoji(image=response, name=name)
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(), description=f"**{ctx.author}**, I have uploaded the emoji {str(emoji)} to this server!")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Emojis(bot))