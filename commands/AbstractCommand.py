from abc import ABC, abstractmethod
from typing import List
import discord


class AbstractCommand(ABC):

    def __init__(self, message, args, client):
        self.message = message
        self.args = args
        self.client = client

    @abstractmethod
    async def exec(self):
        pass
