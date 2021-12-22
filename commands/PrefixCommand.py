import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils


class PrefixCommand(AbstractCommand):

    async def exec(self):
        txt_channel = self.message.channel
        guild_id = str(self.message.guild.id)
        if len(self.args) == 1:
            prefix = self.client.settings['guilds'][guild_id]['prefix']
            await txt_channel.send(f"Le préfix de commande est : *{prefix}*")
        elif len(self.args) == 2:
            self.client.settings['guilds'][guild_id]['prefix'] = self.args[1]
            await txt_channel.send(f"Le nouveau préfix de commande de ce serveur est : *{self.args[1][0]}*")