import asyncio
import random
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from const import COLOR


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="game", description="game related commands.")
    async def game(self, ctx):
        ...

    @game.command(description="Plays a rock, paper, scissors with the bot.")
    @app_commands.describe(user_choice="Select your choice (blank for random).")
    async def rps(
        self,
        ctx,
        user_choice: Literal["rock", "paper", "scissors", "random"],
    ):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if user_choice == "random":
            user_choice = random.choice(["rock", "paper", "scissors"])

        if user_choice == bot_choice:
            rps_output = "We tied!"
        elif user_choice == "rock" and bot_choice == "scissors":
            rps_output = "You won!"
        elif user_choice == "scissors" and bot_choice == "paper":
            rps_output = "You won!"
        elif user_choice == "paper" and bot_choice == "rock":
            rps_output = "You won!"
        else:
            rps_output = "Bot won!"

        rps_embed = discord.Embed(
            title="Rock Paper Scissors... Shoot!",
            description=f"Bot chooses ***{bot_choice.capitalize()}***\nUser chooses ***{user_choice.capitalize()}***\n\n{rps_output}",
            color=COLOR,
        )
        await ctx.send(embed=rps_embed)

    @game.command(description="Guess a number from a given limit.")
    @app_commands.describe(limit="Enter a limit (default to 30).")
    async def guess(self, ctx, limit: Optional[int] = 30):
        await ctx.send(f"Guess a number from 1 to {limit}")

        random_number = random.randint(1, limit)

        start_time = time.time()
        elapsed_time = 0
        timeout = 20

        while True:
            try:
                response = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.channel.id == ctx.channel.id
                    and m.author.id == ctx.author.id,
                    timeout=timeout - elapsed_time,
                )
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="Time's up",
                    description=f"Sorry, but the correct answer was **{random_number}**.",
                    color=discord.Color.from_rgb(237, 237, 237),
                )
                await ctx.send(embed=timeout_embed)
                break

            try:
                if int(response.content) == random_number:
                    await response.add_reaction("✅")
                    break
            except Exception as e:
                print(e)
                pass

            elapsed_time = time.time() - start_time


async def setup(bot):
    await bot.add_cog(Game(bot))
