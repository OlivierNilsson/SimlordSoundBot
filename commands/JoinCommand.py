import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils


class JoinCommand(AbstractCommand):

    @classmethod
    async def exec(cls):
        users_vc = Utils.get_vc_from_message(cls.message)
        if users_vc is not None:
            for v_client in cls.client.voice_clients:
                if v_client.guild == cls.message.guild and users_vc != v_client.channel:
                    await v_client.move_to(users_vc)
                    return
            await users_vc.connect()
