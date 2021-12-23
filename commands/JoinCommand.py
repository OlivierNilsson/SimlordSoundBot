import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils


class JoinCommand(AbstractCommand):

    async def exec(self):
        users_vc = Utils.get_vc_from_message(self.message)
        if users_vc is not None:
            for v_client in self.client.voice_clients:
                if v_client.guild == self.message.guild and users_vc != v_client:
                    await v_client.move_to(users_vc)
                    return
            await users_vc.connect()
