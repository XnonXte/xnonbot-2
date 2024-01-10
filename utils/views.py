import discord

from const import DISCORD_URL


class HelpViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(label="Discord", url=DISCORD_URL),
        )
        self.add_item(
            discord.ui.Button(
                label="GitHub", url="https://github.com/XnonXte/XnonBot-Rewritten"
            )
        )
