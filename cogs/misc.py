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

    @commands.command(name='say')
    @commands.is_owner()
    async def say_something(self, ctx: Context, *, sentence: str):
        """Make the bot say something.
        
        `sentence` **->** The sentence you want the bot to say.
        """

        await ctx.message.delete()

        await ctx.send(sentence)

def setup(bot: Askro):
    bot.add_cog(Misc(bot))