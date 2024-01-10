"""
Copyright (c) 2023-Present XnonXte

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


class XnonBot(commands.Bot):
    async def setup_hook(self):
        failed = []
        for ext in os.listdir("exts"):
            for cog in os.listdir(f"exts/{ext}"):
                try:
                    if cog.endswith(".py") and cog != "__init__.py":
                        await self.load_extension(f"exts.{ext}.{cog[:-3]}")
                        print(f"{cog} successfully loaded!")
                except Exception as e:
                    print(e)
                    failed.append(cog)
        if failed:
            print(f"The following cog(s) failed to load: {failed}")


load_dotenv(".env")
token = os.getenv("TOKEN")
prefix = ";"

bot = XnonBot(
    command_prefix=commands.when_mentioned_or(prefix),
    intents=discord.Intents.all(),
    help_command=None,
)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} - discord {discord.__version__}")
    await bot.change_presence(activity=discord.Game(name=f"{prefix}help or /help"))


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found: `{ctx.message.content.lstrip(prefix)}`")
    elif isinstance(error, commands.NotOwner):
        await ctx.send(f"You're not the owner! Error: `{error}`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Missing permission(s)! Error: `{error}`")
    elif isinstance(error, commands.BadLiteralArgument):
        await ctx.send(f"Bad literal argument(s)! Error: `{error}`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing the required argument(s)! Error: `{error}`")
    else:
        raise error


bot.run(token)
