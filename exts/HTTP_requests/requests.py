from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from utils import constants, get_requests


class Requests(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="req", description="requests related commands")
    async def req(self, ctx):
        ...

    @req.command(description="Returns a picture of dog.")
    async def dog(self, ctx):
        dog = get_requests.Requests.get_dog_pic()
        dog_embed = discord.Embed(title="Bark! 🐶", color=constants.COLOR)
        dog_embed.set_image(url=dog)
        await ctx.send(embed=dog_embed)

    @req.command(description="Returns a picture of cat.")
    async def cat(self, ctx):
        cat = get_requests.Requests.get_cat_pic()
        cat_embed = discord.Embed(title="Meow! 🐱", color=constants.COLOR)
        cat_embed.set_image(url=cat)
        await ctx.send(embed=cat_embed)

    @req.command(description="Returns a quote from zenquote.io")
    async def quote(self, ctx):
        quote = get_requests.Requests.get_quote()
        quote_embed = discord.Embed(
            title=None,
            description=f"{quote[1]} -{quote[0]}.",
            color=constants.COLOR,
        )
        await ctx.send(embed=quote_embed)

    @req.command(description="Returns a waifu picture from waifu.pics")
    @app_commands.describe(
        category="Choose a category (only 25 because discord choices must be 25 or fewer in length)."
    )
    async def waifu(
        self,
        ctx,
        category: Literal[
            "waifu",
            "neko",
            "shinobu",
            "megumin",
            "bully",
            "cuddle",
            "cry",
            "hug",
            "awoo",
            "kiss",
            "lick",
            "pat",
            "smug",
            "bonk",
            "yeet",
            "blush",
            "smile",
            "wave",
            "highfive",
            "handhold",
            "nom",
            "bite",
            "glomp",
            "slap",
            "kill",
        ],
    ):
        waifu = get_requests.Requests.get_waifu_pic(category)
        waifu_embed = discord.Embed(
            title=f"{category} Generated", color=constants.COLOR
        )
        waifu_embed.set_image(url=waifu)
        await ctx.send(embed=waifu_embed)

    @req.command(description="Gets a random dad joke.")
    async def dadjk(self, ctx):
        dad_joke = get_requests.Requests.get_dad_joke()
        dad_joke_embed = discord.Embed(
            title=None,
            description=dad_joke,
            color=constants.COLOR,
        )
        await ctx.send(embed=dad_joke_embed)

    @req.command(description="Gets a random would you rather question.")
    async def wyr(self, ctx):
        wyr = get_requests.Requests.get_would_you_rather()
        wyr_embed = discord.Embed(title=None, description=wyr, color=constants.COLOR)
        await ctx.send(embed=wyr_embed)


async def setup(bot):
    await bot.add_cog(Requests(bot))
