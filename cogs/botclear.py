import datetime
import random

import discord
from discord.ext import commands

from cogs.utils.embed import EmbedUtils


class Botclear:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bc'])
    async def botclear(self, ctx, amount: int = None):
        owners = [409258904053350400, 240855733208481792]
        if amount is None:
            amount = 100
        if not ctx.author.guild_permissions.manage_messages and not ctx.author.id in owners:
            await ctx.send("Hold on!\nYou require `manage messages` permissions to execute this command!🚫")
            return
        if ctx.author.id in owners or ctx.author.guild_permissions.manage_messages:
            try:
                mgs = await ctx.channel.purge(limit=amount, check=lambda msg: msg.author.bot)
                embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                                      description=f"✅ Succesfully deleted `{len(mgs)}` message(s)!")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                msg = await ctx.send(embed=embed)
                await msg.delete()
                await ctx.message.delete()
            except discord.errors.Forbidden:
                embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                                      description="🚫 I require `manage messages` permissions to execute this command!")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Botclear(bot))
