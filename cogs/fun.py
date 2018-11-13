import asyncio
import datetime
import json
from io import BytesIO

import aiohttp

import discord
from PIL import Image
from discord.ext import commands

from cogs.utils.embed import EmbedUtils


class Fun:
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

    @commands.command()
    async def shit(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get(member.avatar_url_as(format='png', size=512)) as resp:
                response = await resp.read()

        with Image.open("assets/shit.jpg") as im:
            img = Image.open(BytesIO(response))
            imgresized = img.resize((80, 80))
            returnb = BytesIO()
            mergedshit = im.copy()
            mergedshit.paste(imgresized, ((290, 700)))
            mergedshit.save(returnb, 'png')
        returnb.seek(0)
        await ctx.send(file=discord.File(fp=returnb, filename="shit.png"))


    @commands.command()
    async def coffee(self, ctx):
        async with aiohttp.ClientSession().get(ctx.author.avatar_url_as(format="png", size=256)) as r:
            response = await r.read()
        webhook = await ctx.channel.create_webhook(name=ctx.author.display_name, avatar=response)
        await webhook.send(f"Hey {self.bot.user.mention}, I'm really tired now from working. I need a break, would you like to server me a coffee please?")
        await ctx.send("Sure!")
        await ctx.send("Cold or hot?")
        msg1 = await self.bot.wait_for('message', check=lambda msg: msg.channel == ctx.channel and msg.author == ctx.author)
        await ctx.send(f"Alright! I'm gonna serve it {msg1.content} for you!")
        await asyncio.sleep(2.5)
        msg = await ctx.send("*Gets the coffee powder*")
        await asyncio.sleep(2.5)
        await msg.edit(content="*Gets a glass*")
        await asyncio.sleep(2.5)
        await msg.edit(content="*Gets milk*")
        await asyncio.sleep(2.5)
        await msg.edit(content=f"***SMASHES** everything together* and TADAAA! A {msg1.content} coffee for you sir!☕☕")
        await asyncio.sleep(1.5)
        await webhook.send(f"Thank you {self.bot.user.mention}!")
        await asyncio.sleep(2.5)
        await webhook.send(f"*Tries out the coffee* and {self.bot.user.name} got another fan!☕")
        await webhook.delete()
    @commands.command()
    async def mimic(self, ctx, member: discord.Member, *, message: str):
        async with aiohttp.ClientSession().get(member.avatar_url_as(format="png", size=256)) as r:
            resp = await r.read()
        webhook = await ctx.channel.create_webhook(name=member.display_name, avatar=resp)
        await webhook.send(message)
        await webhook.delete()

def setup(bot):
    bot.add_cog(Fun(bot))
