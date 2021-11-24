import discord

class Utils:

    @staticmethod
    def get_vc_from_message(message: discord.Message):
        return message.author.voice.channel