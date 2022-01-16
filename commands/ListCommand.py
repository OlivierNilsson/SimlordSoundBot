import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from utils import Utils
import os


class ListCommand(AbstractCommand):

    async def exec(self):
        guild_id = str(self.message.guild.id)
        increment = 10
        page = 1
        try:
            if self.args[0] == '-p':
                page = int(self.args[1])
        except IndexError:
            pass
        _max = page * increment
        _min = _max - increment
        guild_name = self.message.guild.name
        output = f'```\nSaved sound for {guild_name}:\n\n'
        files = os.listdir(f'sounds/{guild_id}/')
        kept_files: List[str] = []
        for file in files[_min:]:
            if '_del_' not in file:
                kept_files.append(' - ' + file.replace('.mp3', ''))
            if len(kept_files) >= 10:
                break
        file_str = '\n'.join(kept_files)
        output += f'{file_str}\n\n-list -p (page_num) pour naviguer entre les pages```'

        txt_channel = self.message.channel
        await txt_channel.send(output)

