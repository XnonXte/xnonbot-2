from typing import Optional, Literal
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import constants


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="mod", description="moderation related commands.")
    async def mod_command(self, ctx):
        ...

    @mod_command.command(description="Adds a role to a user.")
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(member="Member to assign the role to.", role="Role to add.")
    async def addroleuser(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been given the {role.name} role.")

    @mod_command.command(description="Removes a role from a user.")
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(
        member="Member to remove the role to.", role="Role to remove."
    )
    async def rmroleuser(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} no longer has the {role.name} role.")

    @mod_command.command(description="Creates a new role.")
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(
        reason="The reason for creating the role (shows up on the audit log.).",
        name="The name of the role.",
        permission="The permission(s) for the role (this refer to the method on discord.Permissions).",
        color="Color for the role (must be hex code).",
        hoist="Option whether or not the role should be displayed separately from online/offline members.",
        mentionable="Option whether the role should be mentionable or not.",
    )
    async def mkrole(
        self,
        ctx,
        name: str,
        permission: Literal[
            "advanced",
            "all",
            "all_channel",
            "elevated",
            "general",
            "membership",
            "none",
            "stage",
            "stage_moderator",
            "text",
            "voice",
        ],
        color: str,
        hoist: Optional[bool] = False,
        mentionable: Optional[bool] = False,
        reason: Optional[str] = None,
    ):
        def hex_to_rgb(value):
            value = value.lstrip("#")
            lv = len(value)
            return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))

        permissions_dict = {
            "advanced": discord.Permissions.advanced(),
            "all": discord.Permissions.all(),
            "all_channel": discord.Permissions.all_channel(),
            "elevated": discord.Permissions.elevated(),
            "general": discord.Permissions.general(),
            "membership": discord.Permissions.membership(),
            "none": discord.Permissions.none(),
            "stage": discord.Permissions.stage(),
            "stage_moderator": discord.Permissions.stage_moderator(),
            "text": discord.Permissions.text(),
            "voice": discord.Permissions.voice(),
        }
        try:
            r, g, b = hex_to_rgb(color)
        except ValueError:
            await ctx.send(f"Invalid hex code!", ephemeral=True)
            return

        try:
            role = await ctx.guild.create_role(
                reason=reason,
                name=name,
                permissions=permissions_dict.get(permission),
                color=discord.Color.from_rgb(r, g, b),
                hoist=hoist,
                mentionable=mentionable,
            )
        except discord.Forbidden as e:
            await ctx.send(
                f"You don't have the proper permission(s) to create this role! Error: `{e}`",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            pass

        success_embed = discord.Embed(
            title="Success!",
            description=f"Successfully created the role **{role.name}** in {ctx.guild.name}.",
            color=constants.COLOR,
        )

        await ctx.send(embed=success_embed)

    @mod_command.command(description="Creates a new channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(
        reason="The reason for creating this channel (shows up on the audit log).",
        name="The name of this channel.",
        category="The category to place the newly created channel under.",
        position="The position in the channel list. This is a number that starts at 0.",
        topic="The channel's topic.",
        slowmode_delay="Specifies the slowmode rate limit for user in this channel, in seconds.",
        nsfw="To mark the channel as NSFW or not.",
    )
    async def mkchannel(
        self,
        ctx,
        name: str,
        category: discord.CategoryChannel,
        topic: str,
        position: Optional[int] = None,
        nsfw: Optional[bool] = False,
        slowmode_delay: Optional[int] = None,
        reason: Optional[str] = None,
    ):
        try:
            channel = await ctx.guild.create_text_channel(
                name=name,
                reason=reason,
                category=category,
                topic=topic,
                nsfw=nsfw,
                slowmode_delay=slowmode_delay,
                position=position,
            )
        except discord.Forbidden as e:
            await ctx.send(
                f"You don't have the proper permission(s) to create this text channel! Error: `{e}`",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            pass

        success_embed = discord.Embed(
            title="Success!",
            description=f"Successfully created the channel **{channel.name}** in {ctx.guild.name}.",
            color=constants.COLOR,
        )

        await ctx.send(embed=success_embed)

    @mod_command.command(description="Creates a new voice channel.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(
        reason="The reason for creating this channel (shows up on the audit log).",
        name="The name of this channel.",
        category="The category to place the newly created channel under.",
        position="The position in the channel list. This is a number that starts at 0.",
        user_limit="The channel’s limit for number of members that can be in a voice channel.",
        bitrate="The channel’s preferred audio bitrate in bits per second.",
        video_quality_mode="The camera video quality for the voice channel’s participants.",
    )
    async def mkvoice(
        self,
        ctx,
        name: str,
        category: discord.CategoryChannel,
        user_limit: Optional[int] = None,
        position: Optional[int] = None,
        bitrate: Optional[int] = 64000,
        video_quality_mode: Optional[
            discord.VideoQualityMode
        ] = discord.VideoQualityMode.auto,
        reason: Optional[str] = None,
    ):
        try:
            vc_channel = await ctx.guild.create_voice_channel(
                name=name,
                reason=reason,
                category=category,
                position=position,
                user_limit=user_limit,
                bitrate=bitrate,
                video_quality_mode=video_quality_mode,
            )
        except discord.Forbidden as e:
            await ctx.send(
                f"You don't have the proper permission(s) to create this voice channel! Error: `{e}`",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            pass

        success_embed = discord.Embed(
            title="Success!",
            description=f"Successfully created the voice channel **{vc_channel.name}** in {ctx.guild.name}.",
            color=constants.COLOR,
        )

        await ctx.send(embed=success_embed)

    @mod_command.command(description="Creates a new category.")
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(
        reason="The reason for creating this channel (shows up on the audit log).",
        name="The name of this channel.",
        position="The position in the channel list. This is a number that starts at 0.",
    )
    async def mkcategory(
        self,
        ctx,
        name: str,
        position: Optional[int] = None,
        reason: Optional[str] = None,
    ):
        try:
            category = await ctx.guild.create_category(
                name=name, reason=reason, position=position
            )
        except discord.Forbidden as e:
            await ctx.send(
                f"You don't have the proper permission(s) to create this category! Error: `{e}`",
                ephemeral=True,
            )
            return
        except discord.HTTPException:
            pass

        success_embed = discord.Embed(
            title="Success!",
            description=f"Successfully created the category **{category.name}** in {ctx.guild.name}.",
            color=constants.COLOR,
        )

        await ctx.send(embed=success_embed)

    @mod_command.command(description="Bans a user.")
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(
        user="The member to ban.",
        reason="The reason of the ban (shows up on the audit log.)",
        delete_messages="The time worth of messages to delete from the user in the guild.",
    )
    async def ban(
        self,
        ctx,
        user: discord.User,
        delete_messages: Literal[
            "Don't delete any",
            "Previous hour",
            "Previous 6 hours",
            "Previous 12 hours",
            "Previous 24 hours",
            "Previous 3 days",
            "Previous 7 days",
        ],
        reason: Optional[str] = None,
    ):
        await ctx.defer()

        delete_messages_duration = {
            "Don't delete any": 0,
            "Previous hour": 3600,
            "Previous 6 hours": 21600,
            "Previous 12 hours": 43200,
            "Previous 24 hours": 86400,
            "Previous 3 days": 259200,
            "Previous 7 days": 604800,
        }

        try:
            await ctx.guild.ban(
                user=user,
                delete_message_seconds=delete_messages_duration.get(delete_messages),
                reason=reason,
            )
        except discord.Forbidden as e:
            await ctx.send(f"An error has occured! Error: `{e}`", ephemeral=True)
            return
        except discord.HTTPException:
            pass

        success_embed = discord.Embed(
            title="Success!",
            description=f"Successfully banned {user.name} from {ctx.guild.name} with the reason: {reason or '-'}.",
            color=constants.COLOR,
        )
        success_embed.set_thumbnail(url=user.avatar.url)
        success_embed.set_author(name=user.name, icon_url=user.avatar.url)
        success_embed.set_footer(
            text=f"User ID: {user.id} - Today at {datetime.now().strftime('%I:%M %p')}"
        )

        await ctx.send(embed=success_embed)

    @mod_command.command(
        description="Returns a list of users that are banned from the server."
    )
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx, limit: Optional[int] = None):
        await ctx.defer()

        bans = {}
        ban_entries = ctx.guild.bans(limit=limit)
        async for entry in ban_entries:
            bans[entry.user.mention] = entry.reason

        bans_description = ""
        for index, (user, reason) in enumerate(bans.items(), start=1):
            bans_description += f"{index}. {user} {f'with the reason: `{reason}`' if reason is not None else 'without reason being specified'}\n"

        bans_embed = discord.Embed(
            title=f"Banned Users in {ctx.guild.name}",
            description=bans_description or "There aren't any :)",
            color=constants.COLOR,
        )
        bans_embed.set_footer(
            text=f"Server ID: {ctx.guild.id} - Today at {datetime.now().strftime('%I:%M %p')}",
            icon_url="attachment://logo.jpg",
        )

        await ctx.send(
            file=discord.File("img/logo.jpg", filename="logo.jpg"), embed=bans_embed
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
