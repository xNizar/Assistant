import discord
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.owners = [409258904053350400, 240855733208481792]

    @commands.command(aliases=['m'])
    async def mute(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.manage_roles and not ctx.author.id in self.owners:
            await ctx.send("Hold on!\nYou require `manage roles` permissions to execute this command!🚫")
            return
        elif ctx.author.id in self.owners:
            global mute_role
            mute_role = await ctx.guild.create_role(name='Muted')
            await mute_role.edit(position=1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10)
            await member.add_roles(mute_role)
            await ctx.send(f"I have muted {member.mention}!🙊")
        elif ctx.author.guild_permissions.manage_roles:
            mute_role = await ctx.guild.create_role(name='Muted')
            await mute_role.edit(position=1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10)
            await member.add_roles(mute_role)
            await ctx.send(f"I have muted {member.mention}!🙊")
    @commands.command(aliases=['um'])
    async def unmute(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.manage_roles and not ctx.author.id in self.owners:
            await ctx.send("Hold on!\nYou require `manage roles` permissions to execute this command!🚫")
            return
        elif ctx.author.id in self.owners:
            await member.remove_roles(mute_role)
            await ctx.send(f"I have muted {member.mention}!🙊")
        elif ctx.author.guild_permissions.manage_roles:
            await mute_role.edit(position=1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10)
            await member.remove_roles(mute_role)
            await ctx.send(f"I have muted {member.mention}!🙊")

def setup(bot):
    bot.add_cog(Moderation(bot))
