import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from commands import JoinCommand, SaveCommand
from utils import Utils
import time
import asyncio

class PlayCommand(AbstractCommand):
    """
        -play {url/filename} [-save] [filename]

    """

    async def exec(self):
        await JoinCommand(self.message, self.args, self.client).exec()
        users_vc = self.client.get_voice_client_from_guild(self.message.guild)
        if users_vc is not None:
            guild_id = str(self.message.guild.id)
            url_name = self.args[0]
            if Utils.check_if_yt_url(url_name):
                if len(self.args) > 1:
                    if self.args[1] == '-save':
                        filename = self.args[2]
                        args = [self.args[0], filename]
                        await SaveCommand(self.message, args, self.client).exec()
                        path = f'{guild_id}/{filename}'
                else:
                    path = f'{guild_id}/_del_{time.time()}'
                Utils.download_yt_mp3_from_url(url_name, path)
                path = path + '.mp3'
            else:
                path = f'{guild_id}/{url_name}.mp3'
            source = discord.FFmpegPCMAudio(f'sounds/{path}')
            users_vc.play(source)
            
            