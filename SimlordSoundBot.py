
import discord
import logging
import json
import os

from typing import Dict
from dotenv import load_dotenv

from commands.AbstractCommand import AbstractCommand
from commands import JoinCommand, PrefixCommand
from dotenv import load_dotenv


class SimlordSoundBot(discord.Client):

    def __init__(self) -> None:
        super().__init__()
        self.commands: Dict[str, AbstractCommand] = {
            'join': JoinCommand,
            'prefix': PrefixCommand,
        }
        load_dotenv()

        self.handle_settings_file()

    def __enter__(self):
        return self

    #  Cleanup when the bot is about to close/disconnect
    def __exit__(self, *args, **kwargs) -> None:
        self.sync_settings()
        self.update_settings()
        del self.commands
        del self.settings
        print("\nBot Offline !")

    async def on_ready(self) -> None:
        print('Bot online !')
        self.sync_settings()

    async def on_guild_join(self, guild):
        #  Adds the new guild to the settings in the memory
        print(f"[{__name__}] Je viens de join {guild.name}({guild.id})")
        self.settings['guilds'][guild.id] = {
            'id': guild.id,
            'name': guild.name,
            'prefix': self.settings['default_prefix']
        }

    async def on_guild_remove(self, guild):
        print(f"[{__name__}] Je viens de leave {guild.name}({guild.id})")
        try:
            del self.settings['guilds'][guild.id]
        except KeyError:
            logging.warning(
                f"[{__name__}] {guild.id} introuvable dans les settings !")

    async def on_message(self, message: discord.Message) -> None:
        if not message.author.bot and message.content[0] == self.settings['guilds'][message.guild.id]['prefix']:
            args = message.content[1:].split(" ")
            if args[0] in self.commands:
                command = self.commands[args[0]]
                command.setup(message, args, self)
                await command.exec()

    def sync_settings(self) -> None:
        #  Make sure that every guild is in the settings
        for guild in self.guilds:
            if str(guild.id) not in self.settings['guilds']:
                self.settings['guilds'][guild.id] = {
                    'id': guild.id,
                    'name': guild.name,
                    'prefix': self.settings['default_prefix']
                }

        #  Remove guilds that are no longer supposed to be in the settings
        keys_to_delete = []
        for guild in self.settings['guilds']:
            if str(guild) not in [str(x.id) for x in self.guilds]:
                keys_to_delete.append(str(guild))
        for key in keys_to_delete:
            del self.settings['guilds'][key]

    def update_settings(self):
        # Writes the settings from memory into the file
        with open('settings.json', 'w+') as settings_file:
            json.dump(self.settings, settings_file, indent=4)

    def handle_settings_file(self):
        # make sure a valid
        settings_filename = os.getenv("SETTINGS")
        settings_filename = settings_filename if settings_filename else 'settings.json'

        if not os.path.isfile(settings_filename):
            self.create_settings_file(settings_filename)

        with open(settings_filename) as f:
            try:
                self.settings = json.load(f)
            except:
                self.create_settings_file(settings_filename)
                self.handle_settings_file()

    def create_settings_file(cls, settings_filename: str) -> None:
        #  Default settings file

        file_content = '{"guilds": {}, "default_prefix": "-"}'
        with open(settings_filename, 'w+') as f:
            f.write(file_content)
