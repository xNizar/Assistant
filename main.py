import datetime
import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from cogs.utils.embed import EmbedUtils
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix=when_mentioned_or(';'))


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    with open("memory.json", "r") as f:
        data = json.load(f)
    if message.content in data['learned'][str(message.guild.id)]:
        await message.channel.send(data['learned'][str(message.guild.id)][message.content])
    await bot.process_commands(message)


@bot.command(hidden=True)
async def logout(ctx):
    owners = [409258904053350400, 240855733208481792]
    if not ctx.author.id in owners:
        return
    try:
        await bot.logout()
        await ctx.message.add_reaction('✅')
    except Exception as e:
        await ctx.send(e)


@bot.command(hidden=True)
async def restart(ctx):
    owners = [409258904053350400, 240855733208481792]
    if not ctx.author.id in owners:
        return
    os.system('restart.sh')
    await bot.logout()
    await ctx.send('Successfully restarted!')


@bot.event
async def on_ready():
    for s in bot.guilds:
        print(f"{s.name} ({s.id})")
    await bot.change_presence(status=discord.Status.dnd,
                              activity=discord.Game(name=";help | Owned by The Rain & The Rainbow"))
    print([c.id for c in bot.get_guild(511289451188584490).text_channels])
    print(await bot.get_channel(511290196470267923).create_invite())


@bot.command()
async def invite(ctx):
    """Just if you want to invite me"""
    embed = discord.Embed(color=EmbedUtils.random_color(),
                          description="Invite **[Assistant](https://discordapp.com/oauth2/authorize?client_id=507971831945494528&permissions=8&scope=bot)** to your server!")
    await ctx.send(embed=embed)


@bot.command()
async def learn(ctx, *, name: str):
    with open("memory.json", "r+") as f:
        data = json.load(f)
        if name in data['learned']:
            embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color,
                                  description="I have learned that already, mate.")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                                  description=f"The name of that, what I have learned is \"{name}\". What about the content?")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            msg = await bot.wait_for('message',
                                     check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
            embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                                  description=f"The name of that, what I have learned is \"{name}\". The content is {msg.content}, should I leave it by that or do you want to cancel it?")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Answer with yes/no | 30 seconds left.", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            def check(msg):
                return msg.content == "yes"

            try:
                await bot.wait_for('message',
                                   check=check, timeout=30)
            except TimeoutError:
                embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                                      description="You did not enter a valid option after 30 seconds so the command has been aborted.")
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="This command has been aborted.", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            try:
                if str(ctx.guild.id) in data['learned']:
                    data['learned'].update({msg.content: name})
                else:
                    data['learned'][ctx.guild.id].update({msg.content: name})
            except KeyError:
                data['learned'][ctx.guild.id] = {}
                data['learned'][ctx.guild.id].update({msg.content: name})
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            f.close()
            embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=EmbedUtils.random_color(),
                                  description="Thanks for teaching me some cool stuff!")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{bot.user.name} has learned something new!", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


bot.remove_command("help")

cogs = [
    "cogs.botclear",
    "cogs.fun",
    "cogs.ping",
    "cogs.shit",
    "cogs.eval",
    'cogs.permissions',
    'cogs.emojis',
    'cogs.help',
    'cogs.moderation'
]

if __name__ in '__main__':
    for extension in cogs:
        bot.load_extension(extension)

bot.run("")
