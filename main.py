from dotenv import load_dotenv
load_dotenv()

import os
from typing import Optional
from datetime import datetime
from collections import Counter
from traceback import format_exception

import disnake
from disnake.ext import commands

import utils
from utils.views.help_command import PaginatedHelpCommand

TOKEN = os.getenv('BOT_TOKEN')


class Askro(commands.Bot):
    def __init__(self):
        super().__init__(
            help_command=PaginatedHelpCommand(),
            command_prefix=('!', '?'),
            case_insensitive=True,
            test_guilds=[1116770122770685982],
            strip_after_prefix=True,
            allowed_mentions=disnake.AllowedMentions(
                roles=False, everyone=False, users=True
            ),
            intents=disnake.Intents.all(),
            max_messages=100000,
            owner_ids=[1116768380402270239, 1116770319802322954]
        )

        self._owner_id = 1116768380402270239
        self._owner_ids = [1116768380402270239, 1116770319802322954]

        self.db: utils.databases.Database = utils.databases.Database()

        self.socket_events = Counter()
        self.execs = {}

        self.load_extension('jishaku')
        os.environ['JISHAKU_NO_DM_TRACEBACK'] = '1'
        os.environ['JISHAKU_FORCE_PAGINATOR'] = '1'
        os.environ['JISHAKU_EMBEDDED_JSK'] = '1'
        os.environ['JISHAKU_EMBEDDED_JSK_COLOR'] = 'blurple'

        self.load_extension('reload_cogs')

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                if 'music' not in filename:
                    self.load_extension(f'cogs.{filename[:-3]}')

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow()

        data: utils.Misc = await utils.Misc.get()
        if data is None:
            data = await utils.Misc().commit()
        for cmd_name in data.disabled_commands:
            cmd = self.get_command(cmd_name)
            if cmd is None:
                data.disabled_commands.remove(cmd_name)
                await data.commit()
            else:
                cmd.enabled = False

    @property
    def _owner(self) -> disnake.User:
        # Only returns my user.
        if self._owner_id:
            return self.get_user(self._owner_id)

    @property
    def _owners(self) -> list[disnake.User]:
        # Returns a list of both owner Users.
        if self._owner_ids:
            return [self.get_user(_id) for _id in self._owner_ids]

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def get_context(self, message, *, cls=utils.Context):
        return await super().get_context(message, cls=cls)

    async def get_webhook(
        self,
        channel: disnake.TextChannel,
        *,
        name: str = "vystalia",
        avatar: disnake.Asset = None,
    ) -> disnake.Webhook:
        """Returns the general bot hook or creates one."""

        webhooks = await channel.webhooks()
        webhook = disnake.utils.find(lambda w: w.name and w.name.lower() == name.lower(), webhooks)

        if webhook is None:
            webhook = await channel.create_webhook(
                name=name,
                avatar=await avatar.read() if avatar else None,
                reason="Used ``get_webhook`` but webhook didn't exist",
            )

        return webhook

    async def reference_to_message(
        self, reference: disnake.MessageReference
    ) -> Optional[disnake.Message]:
        if reference._state is None or reference.message_id is None:
            return None

        channel = reference._state.get_channel(reference.channel_id)
        if channel is None:
            return None

        if not isinstance(channel, (disnake.TextChannel, disnake.Thread)):
            return None

        try:
            return await channel.fetch_message(reference.message_id)
        except disnake.NotFound:
            return None
        
    async def inter_reraise(self, inter, item: disnake.ui.Item, error):
        if isinstance(error, utils.Canceled):
            if inter.response.is_done():
                await inter.followup.send('Canceled.', ephemeral=True)
                return await inter.author.send('Canceled.')
            else:
                await inter.response.send_message('Canceled.', ephemeral=True)
                return await inter.author.send('Canceled.')
        disagree = '<:disagree:938412196663271514>'
        get_error = "".join(format_exception(error, error, error.__traceback__))
        em = disnake.Embed(description=f'```py\n{get_error}\n```')
        await self._owner.send(
            content="**An error occurred with a view for the user "
                    f"`{inter.author}` (**{inter.author.id}**), "
                    "here is the error:**\n"
                    f"`View:` **{item.view.__class__}**\n"
                    f"`Item Type:` **{item.type}**\n"
                    f"`Item Row:` **{item.row or '0'}**",
            embed=em
        )
        fmt = f'> {disagree} An error occurred'
        if inter.response.is_done():
            await inter.followup.send(fmt, ephemeral=True)
        else:
            await inter.response.send_message(fmt, ephemeral=True)


Askro().run(TOKEN)