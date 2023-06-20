import disnake
from disnake.ext import commands

import utils
from utils import Context

from main import Askro


class Moderation(commands.Cog):
    """Staff related commands."""
    def __init__(self, bot: Askro):
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return '🛠️'


def setup(bot: Askro):
    bot.add_cog(Moderation(bot))