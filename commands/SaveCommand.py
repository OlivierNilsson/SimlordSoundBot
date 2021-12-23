import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils
import os

class SaveCommand(AbstractCommand):
    """
        SaveCommand

        -save {url} {name}
    """
    error_msg: str = ''

    
    async def exec(self):
        if self.validate_command():
            self.create_guild_folder()
            url = self.args[0]
            filename = self.args[1]
            guild_id = str(self.message.guild.id)
            path = f'{guild_id}/{filename}'
            Utils.download_yt_mp3_from_url(url, path)
        else:
            await self.message.reply(self.error_msg)

    def create_guild_folder(self) -> None:
        guild_id = str(self.message.guild.id)
        path = f'sounds/{guild_id}'
        if not os.path.isdir(path):
            os.makedirs(path)

    def validate_command(self) -> bool:
        if len(self.args) != 2:
            self.error_msg = 'Il manque des arguments ! (-save {url} {name})'
            return False
        if not Utils.check_if_yt_url(self.args[0]):
            self.error_msg = "L'url n'est pas valide ! (https://www.youtube.com/watch?v={video_id})"
            return False
        return True




