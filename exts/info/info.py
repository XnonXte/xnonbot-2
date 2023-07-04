from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import constants, views


MAIN_COMMANDS = """
`help` - Shows the list of available commands you can use.
`/req` - Requests related commands.
` ⤷dog` - Returns a picture of dog.
` ⤷cat` - Returns a picture of cat.
` ⤷quote` - Returns a quote from zenquote.io
` ⤷waifu` - Returns a waifu picture from waifu.pics
` ⤷dadjk` - Gets a random dad joke.
` ⤷wyr` - Gets a random would you rather question.
`/game` - Game related commands.
` ⤷rps` - Plays rock, paper, scissors with the bot.
` ⤷guessnumber` - Guess a number from a given limit.
`/util` - Utility related commands.
` ⤷roll` - Returns a random dice roll.
` ⤷reminder` - Sets a reminder for yourself.
"""

MOD_COMMANDS = """
`/mod` - Moderation related commands.
` ⤷addroleuser` - Adds a role to a user.
` ⤷rmroleuser` - Removes a role from a user.
` ⤷mkrole` - Creates a new role.
` ⤷mkchannel` - Creates a new channel.
` ⤷mkvoice` - Creates a new voice channel.
` ⤷mkcategory` - Creates a new category.
` ⤷ban` - Ban a member.
` ⤷bans` - Returns the list of banned members in the server.
"""

CONFIG_COMMANDS = """
`/config` - Config related commands.
` ⤷ping` - Returns the bot's ping.
` ⤷sync` - Syncs slash commands into tree (owner only command).
"""


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        description="Shows the list of available commands you can use."
    )
    async def help(self, ctx):
        help_embed = discord.Embed(
            title="About XnonBot",
            color=constants.COLOR,
            description="XnonBot is a general-purpose discord bot developed by XnonXte.",
            url="https://github.com/XnonXte/XnonBot-Rewritten",
        )
        help_embed.add_field(name="Commands", value=MAIN_COMMANDS)
        help_embed.add_field(
            name="Moderator Commands", value=MOD_COMMANDS, inline=False
        )
        help_embed.add_field(
            name="Config Commands", value=CONFIG_COMMANDS, inline=False
        )
        help_embed.set_footer(
            text=f"XnonBot {constants.VERSION} - Developed with 💖 by XnonXte.",
            icon_url="attachment://logo.jpg",
        )

        await ctx.send(
            file=discord.File("img/logo.jpg", filename="logo.jpg"),
            embed=help_embed,
            view=views.HelpViews(),
        )

    @commands.hybrid_command(description="Returns the information of a specified user.")
    @app_commands.describe(member="The user to get the information.")
    async def userinfo(self, ctx, member: discord.Member):
        await ctx.defer()

        userinfo_embed = discord.Embed(
            title=None,
            description=member.mention,
            color=member.accent_color or constants.COLOR,
        )
        userinfo_embed.add_field(
            name="Joined At", value=member.joined_at.strftime("%B %d, %Y")
        )
        userinfo_embed.add_field(
            name="Registered", value=member.created_at.strftime("%B %d, %Y")
        )
        userinfo_embed.add_field(
            name="Nitro Since",
            value=member.premium_since.strftime("%B %d, %Y")
            if member.premium_since is not None
            else "None",
        )
        userinfo_embed.add_field(name="Nick", value=member.nick or "None")
        userinfo_embed.add_field(
            name="Activity", value=ctx.guild.get_member(member.id).activity or "None"
        )
        userinfo_embed.add_field(
            name="Status",
            value=str(ctx.guild.get_member(member.id).status).capitalize(),
        )
        userinfo_embed.add_field(
            name=f"Roles [{len(member.roles) - 1}]",  # Excluding @everyone role.
            value=" ".join([role.mention for role in member.roles[1:]]) or "None",
            inline=False,
        )
        userinfo_embed.add_field(
            name="Permissions",
            value=", ".join(
                [
                    str(perm[0]).replace("_", " ").title()
                    for perm in member.guild_permissions
                    if perm[1]
                ]
            ),
            inline=False,
        )
        userinfo_embed.set_author(name=member.name, icon_url=member.avatar.url)
        userinfo_embed.set_thumbnail(url=member.avatar.url)
        userinfo_embed.set_footer(
            text=f"ID: {member.id} - Today at {datetime.now().strftime('%I:%M %p')}",
            icon_url="attachment://logo.jpg",
        )
        await ctx.send(
            file=discord.File("img/logo.jpg", filename="logo.jpg"), embed=userinfo_embed
        )

    @commands.hybrid_command(description="Returns the information about this server")
    async def serverinfo(self, ctx):
        await ctx.defer()

        guild = ctx.guild

        serverinfo_embed = discord.Embed(title=None, color=constants.COLOR)
        serverinfo_embed.add_field(name="Owner", value=guild.owner.name, inline=True)
        serverinfo_embed.add_field(
            name="Members", value=guild.member_count, inline=True
        )
        serverinfo_embed.add_field(
            name="Bans",
            value=len(([entry async for entry in guild.bans(limit=1000)])),
        )
        serverinfo_embed.add_field(name="Categories", value=len(guild.categories))
        serverinfo_embed.add_field(name="Text Channels", value=len(guild.channels))
        serverinfo_embed.add_field(
            name="Voice Channels", value=len(guild.voice_channels)
        )
        serverinfo_embed.add_field(
            name="Roles", value=len(guild.roles) - 1
        )  # Excluding @everyone.
        serverinfo_embed.add_field(name="Emojis", value=len(guild.emojis))
        serverinfo_embed.add_field(name="Stickers", value=len(guild.stickers))
        serverinfo_embed.set_author(name=guild.name, icon_url=guild.icon.url)
        serverinfo_embed.set_thumbnail(url=guild.icon.url)
        serverinfo_embed.set_footer(
            text=f"ID: {guild.id} - Created at {guild.created_at.strftime('%m/%d/%Y %I:%M %p')}",
            icon_url="attachment://logo.jpg",
        )

        await ctx.send(
            file=discord.File("img/logo.jpg", filename="logo.jpg"),
            embed=serverinfo_embed,
        )


async def setup(bot):
    await bot.add_cog(Info(bot))
