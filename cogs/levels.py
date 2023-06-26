import disnake
from disnake.ext import commands

import utils
from utils import Level

from main import Askro


class Levels(commands.Cog):
    """Level and message related commands."""
    def __init__(self, bot: Askro):
        self.bot = bot

    @property
    def display_emoji(self) -> disnake.PartialEmoji:
        return disnake.PartialEmoji(name='super_mario_green_shroom', id=938412194700341350)

    @commands.Cog.listener('on_message')
    async def update_data(self, message: disnake.Message):
        if not message.author.bot and message.guild:
            data: Level = await self.bot.db.get('level', message.author.id)
            if data is None:
                return await self.bot.db.add('levels', Level(id=message.author.id, xp=5, messages_count=1))
            if message.author.id in self.bot.owner_ids:
                data.xp += 30
            else:
                if message.channel.id not in (utils.Channels.bots, utils.Channels.memes):
                    if utils.ExtraRoles.server_booster in (r.id for r in message.author.roles):
                        data.xp += 10
                    else:
                        data.xp += 5
            data.messages_count += 1
            await data.commit()

            lvl = 0
            xp = data.xp
            while True:
                if xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
            if xp < 0:
                lvl = lvl - 1

            if message.author.id not in self.bot.owner_ids:
                if lvl >= 10:
                    guild = self.bot.get_guild(1116770122770685982)
                    role = guild.get_role(1123011914981716018)  # Pic Perms role

                    if role.id not in [r.id for r in message.author.roles]:
                        roles = list(message.author.roles) + [role]
                        await message.author.edit(roles=roles)

                        await utils.try_dm(
                            message.author,
                            content=f'Congratulations of reaching level **10** in `{guild.name}`, '
                                    'you have now unlocked the role **Pic Perms** which '
                                    'allows you to send gifs and images/videos in every channel '
                                    'you have access to chat in.'
                        )

    @commands.slash_command(name='level')
    async def level(self, inter):
        pass

    @level.sub_command(name='view')
    async def level_view(
        self,
        inter: disnake.AppCmdInter,
        member: disnake.Member = commands.Param(lambda inter: inter.author)
    ):
        """View your current level or somebody else's."""

        await inter.response.defer()

        if inter.channel.id not in (1116854686759268352, 1117148228941525012, 1116786173621309481):
            if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
                return await inter.send(
                    f'{self.bot.denial} This command can only be used in <#{utils.Channels.bots}>',
                    ephemeral=True
            )

        if member.bot:
            return await inter.send(
                f'{self.bot.denial} Bot\'s do not have levels!',
                ephemeral=True
            )

        data: Level = await self.bot.db.get('level', member.id)
        if data is None:
            return await inter.send(
                f'{self.bot.denial} User not in the database!',
                ephemeral=True
            )

        rank = 0
        async for _rank in Level.find().sort('xp', -1):
            rank += 1
            if data.id == _rank.id:
                break

        lvl = 0
        xp = data.xp
        while True:
            if xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                break
            lvl += 1
        xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
        if xp < 0:
            lvl = lvl - 1
            xp = data.xp
            xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
        if str(xp).endswith(".0"):
            x = str(xp).replace(".0", "")
            x = int(x)
        else:
            x = int(xp)

        guild = self.bot.get_guild(1116770122770685982)

        current_xp = x
        needed_xp = int(200 * ((1 / 2) * lvl))
        percent = round(float(current_xp * 100 / needed_xp), 2)
        members_count = len([m for m in guild.members if not m.bot])

        rank_card = await (await utils.run_in_executor(utils.create_rank_card)(
            member, lvl, rank, members_count, current_xp, needed_xp, percent
        ))
        await inter.send(file=rank_card)

    @level.sub_command(name='set')
    async def level_set(
        self,
        inter: disnake.AppCmdInter,
        level: int = commands.Param(ge=1, le=900),  # From 1 to 900 including those 2 as well.
        member: disnake.Member = commands.Param(lambda inter: inter.author)
    ):
        """Set the level for a member."""

        if member.id not in self.bot.owner_ids:
            return await inter.send(
                f'{self.bot.denial} Only owners can use this command.'
            )

        xp = ((50 * ((level - 1)**2)) + (50 * (level - 1)))
        data: Level = await self.bot.db.get('level', member.id)
        if data is not None:
            data.xp = xp
            await data.commit()
            return await inter.send(f'> {self.bot.agree} Successfully set `{member.display_name}` to level **{level}**')
        await inter.send(
            f'{self.bot.denial} Member not in the database.',
            ephemeral=True
        )

    @level.sub_command(name='leaderboard')
    async def level_top(self, inter: disnake.AppCmdInter):
        """See the top people with the highest levels."""

        if inter.channel.id not in (1116854686759268352, 1117148228941525012, 1116786173621309481):
            if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
                return await inter.send(
                    f'{self.bot.denial} This command can only be used in <#{utils.Channels.bots}>',
                    ephemeral=True
            )

        guild = self.bot.get_guild(1116770122770685982)

        entries = []
        index = 0
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        level_entries = await self.bot.db.find_sorted('level', 'xp', 0)
        for entry in level_entries:
            entry: Level

            index += 1
            lvl = 0
            while True:
                if entry.xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                    break
                lvl += 1
            user = guild.get_member(entry.id)
            if index in (1, 2, 3):
                place = top_3_emojis[index]
            else:
                place = f'`#{index:,}`'

            if user.id == inter.author.id:
                to_append = (f"**{place} {user.display_name} (YOU)**", f"Level: `{lvl}`\nTotal XP: `{entry.xp:,}`")
                entries.append(to_append)
            else:
                to_append = (f"{place} {user.display_name}", f"Level: `{lvl}`\nTotal XP: `{entry.xp:,}`")
                entries.append(to_append)

        source = utils.FieldPageSource(entries, per_page=10)
        source.embed.title = 'Rank Leaderboard'
        pages = utils.RoboPages(source, ctx=inter)
        await pages.start()

    @commands.slash_command(name='messages')
    async def messages(self, inter):
        pass

    @commands.slash_command(name='view')
    async def messages_view(
        self,
        inter: disnake.AppCmdInter,
        member: disnake.Member = commands.Param(lambda inter: inter.author)
    ):
        """View yours or somebody else's total messages."""

        if inter.channel.id not in (1116854686759268352, 1117148228941525012, 1116786173621309481):
            if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
                return await inter.send(
                    f'{self.bot.denial} This command can only be used in <#{utils.Channels.bots}>',
                    ephemeral=True
            )

        user_db: Level = await self.bot.db.get('level', member.id)
        if user_db is None:
            return await inter.send(
                f'`{member.display_name}` sent no messages.',
                ephemeral=True
            )
        rank = 0
        entries = await self.bot.db.find_sorted('level', 'messages_count', 0)
        for entry in entries:
            rank += 1
            if entry.id == user_db.id:
                break
        em = disnake.Embed(color=utils.blurple)
        em.set_author(name=f'{member.display_name}\'s message stats', icon_url=member.display_avatar)
        em.add_field(name='Total Messages', value=f"`{user_db.messages_count:,}`")
        em.add_field(name='Rank', value=f"`#{rank:,}`")
        em.set_footer(text=f'Requested by: {inter.author.display_name}')
        await inter.send(embed=em)

    @messages.sub_command(name='leaderboard')
    async def msg_top(self, inter: disnake.AppCmdInter):
        """See a top of most active users."""

        if inter.channel.id not in (1116854686759268352, 1117148228941525012, 1116786173621309481):
            if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
                return await inter.send(
                    f'{self.bot.denial} This command can only be used in <#{utils.Channels.bots}>',
                    ephemeral=True
            )

        guild = self.bot.get_guild(1116770122770685982)

        index = 0
        data = []
        top_3_emojis = {1: '🥇', 2: '🥈', 3: '🥉'}
        entries = await self.bot.db.find_sorted('level', 'messages_count', 0)

        for entry in entries:
            entry: Level

            if entry.messages_count != 0:
                index += 1
                mem = guild.get_member(entry.id)
                if index in (1, 2, 3):
                    place = top_3_emojis[index]
                else:
                    place = f'`#{index:,}`'
                if mem.id == inter.author.id:
                    to_append = (f'**{place} {mem.display_name} (YOU)**', f'**{entry.messages_count:,}** messages')
                    data.append(to_append)
                else:
                    to_append = (f'{place} {mem.display_name}', f'**{entry.messages_count:,}** messages')
                    data.append(to_append)

        source = utils.FieldPageSource(data, per_page=10)
        source.embed.title = 'Top Most Active Users'
        pages = utils.RoboPages(source, ctx=inter)
        await pages.start()

    @messages.sub_command(name='add')
    async def msg_add(
        self,
        inter: disnake.AppCmdInter,
        amount: str,
        member: disnake.Member = commands.Param(lambda inter: inter.author)
    ):
        """Add a certain amount of messages for the member."""

        if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
            return await inter.send(
                f'{self.bot.denial} This command can only be used by admins and above!',
                ephemeral=True
        )

        usr_db: Level = await self.bot.db.get('level', member.id)
        if usr_db is None:
            return await inter.send(
                f'{self.bot.denial} User not in the database.',
                ephemeral=True
            )

        try:
            amount = utils.format_amount(amount)
            amount = int(amount)
        except ValueError:
            return await inter.send(
                f'{self.bot.denial} The amount must be an integer.'
            )

        usr_db.messages_count += amount
        await usr_db.commit()
        await inter.send(f'> {self.bot.agree} Added `{amount:,}` messages to {member.mention}')

    @messages.sub_command(name='set')
    async def msg_set(
        self,
        inter: disnake.AppCmdInter,
        amount: str,
        member: disnake.Member = commands.Param(lambda inter: inter.author)
    ):
        """Set the amount of messages for the member."""

        if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
            return await inter.send(
                f'{self.bot.denial} This command can only be used by admins and above!',
                ephemeral=True
        )

        usr_db: Level = await self.bot.db.get('level', member.id)
        if usr_db is None:
            return await inter.send(
                f'{self.bot.denial} User not in the database.',
                ephemeral=True
            )

        try:
            amount = utils.format_amount(amount)
            amount = int(amount)
        except ValueError:
            return await inter.send(
                f'{self.bot.denial} The amount must be an integer.',
                ephemeral=True
            )

        usr_db.messages_count = amount
        await usr_db.commit()
        await inter.send(f'> {self.bot.agree} Set the amount of messages for {member.mention} to `{amount:,}` messages.')

    @messages.sub_command(name='reset')
    async def msg_reset(self, inter: disnake.AppCmdInter, member: disnake.Member):
        """Reset the amount of total messages for the member."""

        if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
            return await inter.send(
                f'{self.bot.denial} This command can only be used by admins and above!',
                ephemeral=True
        )

        usr_db: Level = await self.bot.db.get('level', member.id)
        if usr_db is None:
            return await inter.send(
                f'{self.bot.denial} User not in the database.',
                ephemeral=True
            )

        view = utils.ConfirmViewInteraction(inter, f"{inter.author.mention} Did not react in time.")
        await inter.send(
            f"Are you sure you want to reset the total message count for member {member.mention}?",
            view=view
        )
        await view.wait()
        if view.response is True:
            usr_db.messages_count = 0
            await usr_db.commit()
            return await inter.edit_original_message(
                content=f'The total message count for member **{member.display_name}** has been reset successfully.',
                view=view
            )

        elif view.response is False:
            return await inter.edit_original_message(
                content=f"Command to reset the message count for user `{member.display_name}` has been cancelled.",
                view=view
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        if member.guild.id != 1116770122770685982:
            return

        await self.bot.db.delete('levels', {'_id': member.id})


def setup(bot: Askro):
    bot.add_cog(Levels(bot))