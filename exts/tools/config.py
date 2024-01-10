from typing import Literal

from discord.ext import commands
from discord import app_commands


class Config(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="config", description="config related commands.")
    async def cfg(self, ctx):
        ...

    @cfg.command(description="Returns the bot's latency.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! My latency is `{round(self.bot.latency * 100, 2)}`ms")

    @cfg.command(description="Command to sync all slash commands.")
    @app_commands.describe(option="The scope for the bot to sync.")
    @commands.is_owner()
    async def sync(
        self, ctx: commands.Context, option: Literal["local", "clear", "global"]
    ):
        if option == "local":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif option == "clear":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        elif option == "global":
            synced = await ctx.bot.tree.sync()
        await ctx.send(
            f"{len(synced)} command(s) synced {'globally' if option == 'global' else f'to {ctx.guild.name}'}."
        )


async def setup(bot):
    await bot.add_cog(Config(bot))
