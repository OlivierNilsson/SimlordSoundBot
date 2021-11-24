from abc import ABC, abstractmethod
from typing import List
import discord


class AbstractCommand(ABC):

    message: discord.Message = None
    args: List[str] = []
    client: discord.Client = None

    @classmethod
    def setup(cls, message, args, client):
        cls.message = message
        cls.args = args
        cls.client = client

    @classmethod
    @abstractmethod
    async def exec(cls):
        pass
