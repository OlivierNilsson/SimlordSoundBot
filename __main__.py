
import os


from dotenv import load_dotenv

from SimlordSoundBot import SimlordSoundBot




with SimlordSoundBot() as bot:

    print("Starting SimlordSoundBot")

    load_dotenv()
    APP_TOKEN = os.getenv("TOKEN")

    bot.run(APP_TOKEN)