import discord
import os
import youtube_dl


class Utils:

    @staticmethod
    def get_vc_from_message(message: discord.Message):
        return message.author.voice.channel

    @staticmethod
    def download_yt_mp3_from_url(url, filename):

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            "outtmpl": f"sounds/{filename}",
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
