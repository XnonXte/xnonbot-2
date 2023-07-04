import asyncio
import random
from typing import Literal

from discord.ext import commands
from discord import app_commands


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="util", description="utility related commands.")
    async def util(self, ctx):
        ...

    @util.command(description="Sets a reminder for yourself.")
    @app_commands.describe(
        time="The amount of time should the bot wait to send the reminder.",
        reminder="The reminder message.",
    )
    async def reminder(
        self,
        ctx,
        time: Literal[
            "5 minutes",
            "10 minutes",
            "15 minutes",
            "30 minutes",
            "60 minutes",
            "3 hours",
            "6 hours",
            "12 hours",
            "24 hours",
        ],
        reminder: str,
    ):
        time_dict = {
            "5 minutes": 300,
            "10 minutes": 600,
            "15 minutes": 900,
            "30 minutes": 1800,
            "60 minutes": 3600,
            "3 hours": 10800,
            "6 hours": 21600,
            "12 hours": 43200,
            "24 hours": 86400,
        }
        await ctx.send(f"Okay, I will remind you in **{time}**.")
        await asyncio.sleep(time_dict.get(time))
        await ctx.send(f"Reminder for {ctx.author.mention}: `{reminder}`.")

    @util.command(description="Returns a random dice roll.")
    async def roll(self, ctx):
        random_dice_roll = random.randint(1, 6)
        await ctx.send(random_dice_roll)

    @commands.command()
    async def choose(self, ctx, *args):
        output = random.choice((args))
        await ctx.send(f"I choose {output}.")


async def setup(bot):
    await bot.add_cog(Utility(bot))
