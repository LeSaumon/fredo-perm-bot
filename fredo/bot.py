import nextcord
from nextcord.ext import commands


class Fredo(commands.Bot):
    def __init__(self) -> None:
        super().__init__(intents=self._set_intents())

    def _set_intents(self) -> nextcord.Intents:
        intents = nextcord.Intents.default()
        intents.members = True
        intents.messages = True
        return intents


bot = Fredo()
