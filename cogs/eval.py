import io
import textwrap
import traceback
from contextlib import redirect_stdout

import discord
from discord.ext import commands

from cogs.utils.embed import EmbedUtils


class Owner:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(pass_context=True, hidden=True)
    async def eval(self, ctx, *, body: str):
        """Evaluates a code"""
        owners = [240855733208481792, 409258904053350400]
        if not ctx.author.id in owners:
            return
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "self": self,
            "_": self._last_result
        }

        def cleanup_code(content):
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])
        env.update(globals())
        body = cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)

        except Exception as e:
            return await ctx.send (f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            return await ctx.send(f'```py\n{value}{str(traceback.format_exc()).replace("Arash", "User")}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    try:
                        embed = discord.Embed(color=EmbedUtils.random_color(),
                                              description=f":inbox_tray: **Input**\n{ctx.message.content.replace(';eval', '')}\n:outbox_tray: **Output**\n```markdown\n{value}\n```")
                        embed.set_footer(text="Evaluated in " + str(self.bot.latency)[:-13] + " milliseconds",
                                         icon_url="https://images-ext-1.discordapp.net/external/3ySfWfvhv6j0ycZwm6fYA7jcOfrzST69owF2zCYu30I/https/www.python.org/static/opengraph-icon-200x200.png")
                        await ctx.send(embed=embed)
                    except discord.errors.HTTPException:
                        with open("error.txt", "w+") as f:
                            f.write(value)
                        await ctx.send(file=discord.File("error.txt"))

            else:
                _last_result = ret
                try:
                    embed = discord.Embed(color=EmbedUtils.random_color(),
                                          description=f":inbox_tray: **Input**\n{ctx.message.content.replace(';eval', '')}\n:outbox_tray: **Output**\n```markdown\n{value}{ret}\n```")
                    embed.set_footer(text="Evaluated in " + str(self.bot.latency)[:-13] + " milliseconds",
                                     icon_url="https://images-ext-1.discordapp.net/external/3ySfWfvhv6j0ycZwm6fYA7jcOfrzST69owF2zCYu30I/https/www.python.org/static/opengraph-icon-200x200.png")
                    await ctx.send(embed=embed)
                except discord.errors.HTTPException:
                    with open("error.txt", "w+") as f:
                        f.write(f"{value}{ret}")
                    await ctx.send(file=discord.File("error.txt"))
def setup(bot):
    bot.add_cog(Owner(bot))