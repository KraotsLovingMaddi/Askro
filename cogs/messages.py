import asyncio
from datetime import datetime

import disnake
from disnake.ext import commands

import utils

from main import Askro


class Messages(commands.Cog):
    def __init__(self, bot: Askro):
        self.bot = bot

    @commands.Cog.listener('on_message_delete')
    async def on_message_delete(self, message: disnake.Message):
        if message.author.bot or not message.guild:
            return
        if message.author.id == self.bot._owner_id:
            return

        else:
            if not message.content:
                if not message.attachments:
                    return
                if not message.attachments[0].content_type.endswith(('png', 'jpg', 'jpeg')):
                    return

            content = f'```{utils.remove_markdown(message.content)}```' if message.content else '\u200b'
            em = disnake.Embed(
                color=utils.red,
                description=f'Message deleted in <#{message.channel.id}> \n\n'
                            f'**Content:** \n{content}',
                timestamp=datetime.utcnow()
            )
            em.set_author(name=message.author.display_name, icon_url=f'{message.author.display_avatar}')
            em.set_footer(text=f'User ID: {message.author.id}')
            if message.attachments:
                em.set_image(url=message.attachments[0].proxy_url)
            ref = message.reference
            if ref and isinstance(ref.resolved, disnake.Message):
                em.add_field(
                    name='Replying to...',
                    value=f'[{ref.resolved.author}]({ref.resolved.jump_url})',
                    inline=False
                )

            await asyncio.sleep(0.5)
            try:
                btn = disnake.ui.View()
                btn.add_item(disnake.ui.Button(label='Jump!', url=message.jump_url))
                await self.bot.webhooks['message_logs'].send(embed=em, view=btn)
            except Exception as e:
                ctx = await self.bot.get_context(message)
                await ctx.reraise(e)

    @commands.Cog.listener('on_message_edit')
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if before.author.bot or not after.guild:
            return
        if before.author.id == self.bot._owner_id:
            return
        else:
            if before.content == after.content:
                return

            em = disnake.Embed(
                color=utils.yellow,
                description=f'Message edited in <#{before.channel.id}>\n\n'
                            f'**Before:**\n```{utils.remove_markdown(before.content)}```\n\n'
                            f'**After:**\n```{utils.remove_markdown(after.content)}```',
                timestamp=datetime.datetime.utcnow()
            )
            em.set_author(name=before.author.display_name, icon_url=f'{before.author.display_avatar}')
            em.set_footer(text=f'User ID: {before.author.id}')
            ref = after.reference
            if ref and isinstance(ref.resolved, disnake.Message):
                em.add_field(
                    name='Replying to...',
                    value=f'[{ref.resolved.author}]({ref.resolved.jump_url})',
                    inline=False
                )

            await utils.check_username(self.bot, after.author, bad_words=self.bot.bad_words.keys())
            await asyncio.sleep(0.5)
            try:
                btn = disnake.ui.View()
                btn.add_item(disnake.ui.Button(label='Jump!', url=after.jump_url))
                await self.bot.webhooks['message_logs'].send(embed=em, view=btn)
            except Exception as e:
                ctx = await self.bot.get_context(after)
                await ctx.reraise(e)

    @commands.Cog.listener('on_message_edit')
    async def repeat_command(self, before: disnake.Message, after: disnake.Message):
        if not after.content:
            return
        elif after.content[0] not in ('!', '?'):
            return

        ctx = await self.bot.get_context(after)
        cmd = self.bot.get_command(after.content.replace('!', '').replace('?', ''))
        if cmd is None:
            return

        if after.content.lower()[1:].startswith(('e', 'eval', 'jsk', 'jishaku')) and \
            after.author.id == self.bot._owner_id or \
                after.content.lower()[1:].startswith(('run', 'code')):
            await after.add_reaction('🔁')
            try:
                await self.bot.wait_for(
                    'reaction_add',
                    check=lambda r, u: str(r.emoji) == '🔁' and u.id == after.author.id,
                    timeout=360.0
                )
            except asyncio.TimeoutError:
                await after.clear_reaction('🔁')
            else:
                curr: disnake.Message = self.bot.execs[after.author.id].get(cmd.name)
                if curr:
                    await curr.delete()
                await after.clear_reaction('🔁')
                await cmd.invoke(ctx)
            return
        await cmd.invoke(ctx)


def setup(bot: Askro):
    bot.add_cog(Messages(bot))