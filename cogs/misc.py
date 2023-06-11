from disnake.ext import commands

import utils
from utils import Context

from main import Askro


class Misc(commands.Cog):
    """Miscellaneous commands, basically commands that i have no fucking idea where to fucking put so they just come in this category."""
    def __init__(self, bot: Askro):
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return '🔧'


def setup(bot: Askro):
    bot.add_cog(Misc(bot))