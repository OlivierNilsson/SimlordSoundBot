import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils


class PauseCommand(AbstractCommand):

    async def exec(self):
        users_vc = Utils.get_vc_from_message(self.message)
        if users_vc is not None:
            voice_client = self.client.get_voice_client_from_guild(self.message.guild)
            if voice_client.is_playing() and not voice_client.is_paused():
                txt_channel = self.message.channel
                voice_client.pause()
                await txt_channel.send("Paused !")
