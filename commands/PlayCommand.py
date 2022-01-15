import discord
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from commands import JoinCommand, SaveCommand
from utils import Utils
import time


class PlayCommand(AbstractCommand):
    """
        -play {url/filename} [-save] [filename]

    """

    async def exec(self):
        await JoinCommand(self.message, self.args, self.client).exec()
        users_vc = self.client.get_voice_client_from_guild(self.message.guild)
        if users_vc is not None:
            path = await self.download_song()
            path = f'sounds/{path}'
            guild_id = str(users_vc.guild.id)
            self.setup_queue(guild_id)
            self.client.queues[guild_id].append(path)
            if not users_vc.is_playing():
                source = discord.FFmpegPCMAudio(path)
                users_vc.play(source, after=lambda e: self.play_next(guild_id, users_vc))
                await self.message.channel.send("Now Playing ...")
            else:
                await self.message.channel.send("Song Queued ...")

    def play_next(self, guild_id: str, voice_client: discord.VoiceClient):
        if len(self.client.queues[guild_id]) >= 1:
            del self.client.queues[guild_id][0]
            next_song = self.client.queues[guild_id][0]
            source = discord.FFmpegPCMAudio(next_song)
            voice_client.play(source, after=lambda e: self.play_next(guild_id, voice_client))

    def setup_queue(self, guild_id: str):
        if guild_id not in self.client.queues:
            self.client.queues[guild_id] = []

    async def download_song(self) -> str:
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
        return path
