from datetime import datetime

import discord
from discord.ext import commands

from const import COLOR


class Greeting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        if guild.system_channel is not None:
            welcome_embed = discord.Embed(
                title=None,
                description=f"Welcome {member.name}! Enjoy your stay here.",
                color=member.accent_color or COLOR,
            )
            welcome_embed.set_author(name=member.name, icon_url=member.avatar.url)
            welcome_embed.set_thumbnail(url=member.avatar.url)
            welcome_embed.set_footer(
                text=f"Today at {datetime.now().strftime('%I:%M %p')}",
                icon_url="attachment://logo.jpg",
            )
            await guild.system_channel.send(
                f"Everyone welcome {member.mention} to {guild.name}!",
                file=discord.File("img/logo.jpg", filename="logo.jpg"),
                embed=welcome_embed,
            )


async def setup(bot):
    await bot.add_cog(Greeting(bot))
