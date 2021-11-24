import discord
import logging
import json
import os
from typing import Dict
from commands.AbstractCommand import AbstractCommand
from commands import JoinCommand, PrefixCommand
from dotenv import load_dotenv


class SimlordSoundBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.commands: Dict[str, AbstractCommand] = {
            'join': JoinCommand,
            'prefix': PrefixCommand,
        }
        load_dotenv()

        APP_TOKEN = os.getenv("TOKEN")
        with open('settings.json') as f:
            self.settings = json.load(f)
        self.run(APP_TOKEN)

    #  To explore
    def __del__(self):
        # self.update_settings()
        #del self.commands
        #del self.settings
        print("Bot Offline !")

    async def on_ready(self) -> None:
        print('Bot online !')
        self.sync_settings()

    async def on_guild_join(self, guild):
        print(f"[{__name__}] je viens de join {guild.name}({guild.id})")
        self.settings['guilds'][guild.id] = {
            'id': guild.id,
            'name': guild.name,
            'prefix': self.settings['default_prefix']
        }

    async def on_guild_remove(self, guild):
        print(f"[{__name__}] je viens de leave {guild.name}({guild.id})")
        print(self.settings['guilds'].keys())
        try:
            del self.settings['guilds'][str(guild.id)]
        except KeyError:
            logging.warning(
                f"[{__name__}] {guild.id} introuvable dans les settings !")

    async def on_message(self, message: discord.Message) -> None:
        if not message.author.bot and message.content[0] == self.settings['guilds'][str(message.guild.id)]['prefix']:
            args = message.content[1:].split(" ")
            if args[0] in self.commands:
                command = self.commands[args[0]]
                command.setup(message, args, self)
                await command.exec()

    def sync_settings(self) -> None:
        for guild in self.guilds:
            if str(guild.id) not in self.settings['guilds']:
                self.settings['guilds'][guild.id] = {
                    'id': guild.id,
                    'name': guild.name,
                    'prefix': self.settings['default_prefix']
                }
        keys_to_delete = []
        for guild in self.settings['guilds']:
            if str(guild) not in [str(x.id) for x in self.guilds]:
                keys_to_delete.append(str(guild))
        for key in keys_to_delete:
            del self.settings['guilds'][key]
        self.update_settings()

    def update_settings(self):
        with open('settings.json', 'w+') as settings_file:
            json.dump(self.settings, settings_file, indent=4)
