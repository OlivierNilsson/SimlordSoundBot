import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils


class PrefixCommand(AbstractCommand):

    @classmethod
    async def exec(cls):
        txt_channel = cls.message.channel
        guild_id = str(cls.message.guild.id)
        if len(cls.args) == 1:
            prefix = cls.client.settings['guilds'][guild_id]['prefix']
            await txt_channel.send(f"Le préfix de commande est : *{prefix}*")
        elif len(cls.args) == 2:
            cls.client.settings['guilds'][guild_id]['prefix'] = cls.args[1]
            await txt_channel.send(f"Le nouveau préfix de commande de ce serveur est : *{cls.args[1][0]}*")