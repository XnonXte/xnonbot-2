import discord

VERSION = "v0.5.1"
COLOR = discord.Color.from_rgb(50, 100, 255)
MAIN_COMMANDS = """
`help` - Shows the list of available commands you can use.
`info` - Returns the information of a specified user.
`serverinfo` - Returns the information about this server.
`/req` - Requests related commands.
` ⤷dog` - Returns a picture of dog.
` ⤷cat` - Returns a picture of cat.
` ⤷quote` - Returns a quote from zenquote.io
` ⤷waifu` - Returns a waifu picture from waifu.pics
` ⤷dadjk` - Gets a random dad joke.
` ⤷wyr` - Gets a random would you rather question.
`/game` - Game related commands.
` ⤷rps` - Plays rock, paper, scissors with the bot.
` guess` - Guess a number from a given limit.
`/util` - Utility related commands.
` ⤷roll` - Returns a random dice roll.
` ⤷reminder` - Sets a reminder for yourself.
"""
MOD_COMMANDS = """
`/mod` - Moderation related commands.
` ⤷addrole` - Adds a role to a user.
` ⤷rmrole` - Removes a role from a user.
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
DISCORD_URL = "https://discord.gg/dDbgtFb2KC"
