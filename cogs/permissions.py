import datetime
import discord
from discord.ext import commands

from cogs.utils.embed import EmbedUtils


class Permissions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def permissions(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        permissions = ctx.channel.permissions_for(member)
        e = discord.Embed(timestamp=datetime.datetime.utcnow(), title=f"{member.name}'s permissions.",
                          color=EmbedUtils.random_color())
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='<:enabled:504303419603812353>', value='<:enabled:504303419603812353>' + '\n <:enabled:504303419603812353>'.join(allowed), inline=True)
        e.add_field(name='<:disabled:493093839377006602>', value='<:disabled:493093839377006602>' + '\n <:disabled:493093839377006602>'.join(denied), inline=True)
        e.set_footer(text=f"Requested by {ctx.author}", icon_url=member.avatar_url)
        e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Permissions(bot))
