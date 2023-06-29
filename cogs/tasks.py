import disnake
from disnake.ext import commands, tasks

from main import Askro


class Tasks(commands.Cog):
    def __init__(self, bot: Askro):
        self.bot = bot

        self.servers = [
            1123864840922992713, 1123865126022426687, 1123865085316698145,
            1123865167369879582
        ]

        self.notify_bump.start()

    @tasks.loop(seconds=2100.0)
    async def notify_bump(self):
        server = self.servers[0]
        self.servers.append(server)
        self.servers = self.servers[1:]

        guild = self.bot.get_guild(server)
        channel = disnake.utils.find(lambda c: c.name == 'bump', guild.channels)
        if channel:
            await channel.send(
                f'{guild.default_role.mention}\n\n It\'s your turn to bump!\n\n'
                '*If you didn\'t bump within* ***10 minutes*** *from receiving this message, '
                'then wait for the next message '
                'so that you don\'t interfere with the other\'s turns to bump.*',
                allowed_mentions=disnake.AllowedMentions(everyone=True)
            )

    @notify_bump.before_loop
    async def wait_for_ready_bump(self):
        await self.bot.wait_until_ready()


def setup(bot: Askro):
    bot.add_cog(Tasks(bot))