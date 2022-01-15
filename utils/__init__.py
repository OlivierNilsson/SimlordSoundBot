import discord
import os
import youtube_dl
from pytube import YouTube


class Utils:

    @staticmethod
    def get_vc_from_message(message: discord.Message) -> discord.VoiceChannel:
        return message.author.voice.channel

    @staticmethod
    def download_yt_mp3_from_url(url, path):
        yt = YouTube(url)
        print("Downloading ", url)
        path = 'sounds/' + path
        yt.streams.filter(only_audio=True).desc().first().download(filename=path + '.mp3')


    #    print("url: ", url)
    #    path = 'sounds/' + path
    #    print("Path: ", path)
    #    ydl_opts = {
    #        'format': 'bestaudio/best',
    #        'postprocessors': [{
    #            'key': 'FFmpegExtractAudio',
    #            'preferredcodec': 'mp3',
    #            'preferredquality': '192',
    #        }],
    #        "outtmpl": path + ".mp3",
    #        'keepvideo': False,
    #        'noplaylist': True,
    #        'extractaudio': True,
    #    }
    #
    #    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #        ydl.download([url])
    

    @staticmethod
    def check_if_contains_images(message: discord.Message) -> bool:
        return (len(message.attachments) >= 1)

    @staticmethod
    def check_if_yt_url(url: str) -> bool:
        return ('https://www.youtube.com/watch?v=' in url)
