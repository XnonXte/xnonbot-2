from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from const import COLOR, VERSION, MAIN_COMMANDS, MOD_COMMANDS, CONFIG_COMMANDS
from utils import views


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        description="Shows the list of available commands you can use."
    )
    async def help(self, ctx):
        help_embed = discord.Embed(
            title="About XnonBot",
            color=COLOR,
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
            text=f"XnonBot {VERSION} - Developed with 💖 by XnonXte.",
            icon_url="attachment://logo.jpg",
        )

        await ctx.send(
            file=discord.File("img/logo.jpg", filename="logo.jpg"),
            embed=help_embed,
            view=views.HelpViews(),
            ephemeral=True,
        )

    @commands.hybrid_command(description="Returns the information of a specified user.")
    @app_commands.describe(member="The user to get the information.")
    async def info(self, ctx, member: discord.Member):
        await ctx.defer()

        info_embed = discord.Embed(
            title=None,
            description=member.mention,
            color=member.accent_color or COLOR,
        )
        info_embed.add_field(
            name="Joined At", value=member.joined_at.strftime("%B %d, %Y")
        )
        info_embed.add_field(
            name="Registered", value=member.created_at.strftime("%B %d, %Y")
        )
        info_embed.add_field(
            name="Nitro Since",
            value=member.premium_since.strftime("%B %d, %Y")
            if member.premium_since is not None
            else "None",
        )
        info_embed.add_field(name="Nick", value=member.nick or "None")
        info_embed.add_field(
            name="Activity", value=ctx.guild.get_member(member.id).activity or "None"
        )
        info_embed.add_field(
            name="Status",
            value=str(ctx.guild.get_member(member.id).status).capitalize(),
        )
        info_embed.add_field(
            name=f"Roles [{len(member.roles) - 1}]",  # Excluding @everyone role.
            value=" ".join([role.mention for role in member.roles[1:]]) or "None",
            inline=False,
        )
        info_embed.add_field(
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
        info_embed.set_author(name=member.name, icon_url=member.avatar.url)
        info_embed.set_thumbnail(url=member.avatar.url)
        info_embed.set_footer(
            text=f"ID: {member.id} - Today at {datetime.now().strftime('%I:%M %p')}",
            icon_url="attachment://logo.jpg",
        )
        await ctx.send(
            file=discord.File("img/logo.jpg", filename="logo.jpg"), embed=info_embed
        )

    @commands.hybrid_command(description="Returns the information about this server")
    async def serverinfo(self, ctx):
        await ctx.defer()

        guild = ctx.guild

        serverinfo_embed = discord.Embed(title=None, color=COLOR)
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
