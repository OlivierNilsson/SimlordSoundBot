#!/usr/bin/env python

import os

from SimlordSoundBot import SimlordSoundBot
from dotenv import load_dotenv





with SimlordSoundBot() as bot:

    print("Starting SimlordSoundBot")

    load_dotenv()
    APP_TOKEN = os.getenv("TOKEN")

    bot.run(APP_TOKEN)
