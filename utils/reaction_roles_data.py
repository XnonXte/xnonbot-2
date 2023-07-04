import json

# Example JSON file.
# {
# "1103578001318346812": {
#     "1125316343399461005": {
#         discord.PartialEmoji(name="🟢"): 1125311410038120468
#     },
#     "1125316367353122828": {
#         discord.PartialEmoji(name="🟡"): 1125311371794456717
#     },
#     "1125316376324751391": {
#         discord.PartialEmoji(name="🔴"): 1125310842259382383
#     },
# },
# }


class ReactionRoles:
    """Reaction roles related functions."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

    def load_data(self):
        with open(self.filepath, "r") as file:
            self.data = json.load(file)
            return self.data

    def save_data(self):
        with open(self.filepath, "w") as file:
            json.dump(self.data, file)

    def add_reaction_role(self, guild_id, message_id, partial_emoji, role_id):
        """Adding a reaction role to a message."""
        # This ensures everything is in the right data type.
        guild_id, message_id, partial_emoji = (
            str(guild_id),
            str(message_id),
            str(partial_emoji),
        )
        if guild_id not in self.data:
            self.data[guild_id] = {}
        if message_id not in self.data[guild_id]:
            self.data[guild_id][message_id] = {}
        self.data[guild_id][message_id][partial_emoji] = role_id

    def remove_reaction_role(self, guild_id, message_id, partial_emoji):
        guild_id, message_id, partial_emoji = (
            str(guild_id),
            str(message_id),
            str(partial_emoji),
        )
        if guild_id not in self.data:
            raise KeyError("Server not found!")
        if message_id not in self.data[guild_id]:
            raise KeyError("Message not found!")
        if partial_emoji not in self.data[guild_id][message_id]:
            raise KeyError("Reaction role not found!")
        del self.data[guild_id][message_id][partial_emoji]


test = ReactionRoles("database/reaction_roles_data.json")
print(test.load_data()["1103578001318346812"])
