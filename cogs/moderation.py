from datetime import datetime
from dateutil.relativedelta import relativedelta

import disnake
from disnake.ext import commands, tasks

import utils

from main import Askro


class Moderation(commands.Cog):
    """Staff related commands."""
    def __init__(self, bot: Askro):
        self.bot = bot

        self.check_mutes.start()
        self.check_streaks.start()

    async def check_perms(self, inter: disnake.AppCmdInter) -> bool:
        """
        Returns `False` if the user doesn't have enough perms to use this command
        meaning they're not a staff member, otherwise returns `True` if they're a staff member.
        """

        if not any(r for r in utils.StaffRoles.all if r in (role.id for role in inter.author.roles)):
            if inter.author.id not in self.bot.owner_ids:
                await inter.send(
                    f'{self.bot.denial} This command can only be used by admins and above!',
                    ephemeral=True
            )
                return False
        return True

    @property
    def display_emoji(self) -> str:
        return '🛠️'

    @commands.slash_command(name='mute')
    async def mute(
        self,
        inter: disnake.AppCmdInter,
        member: disnake.Member,
        duration: str,
        reason: str
    ):
        """Mutes a member."""

        if await self.check_perms(inter) is False:
            return

        try:
            duration = duration.replace(' ', '')  # This is what caused the TypeError
            time_and_reason = await utils.UserFriendlyTime().convert(duration + ' ' + reason)
            mute_duration = utils.human_timedelta(time_and_reason.dt, suffix=False)
            expiration_date = utils.format_dt(time_and_reason.dt, 'F')
        except commands.BadArgument as e:
            return await inter.send(f'{self.bot.denial} {e}', ephemeral=True)
        except TypeError:
            return await inter.send(f'{self.bot.denial} Invalid time provided.', ephemeral=True)

        if member.top_role >= inter.author.top_role and inter.author.id not in self.bot.owner_ids:
            return await inter.send(
                f'{self.bot.denial} You cannot mute someone that is of higher or equal role to you.',
                ephemeral=True
            )

        had_entry = True
        entry: utils.Mute = await self.bot.db.get('mutes', member.id)
        if entry is None:
            had_entry = False
            entry: utils.Mute = utils.Mute(
                id=member.id,
                muted_by=inter.author.id
            )
        elif entry.is_muted is True:
            return await inter.send(
                f'{self.bot.denial} That member is already muted!',
                ephemeral=True
            )

        staff_rank = 'Apparently not a staff member, please contact the owner about this issue.'
        _author_roles_ids = [r.id for r in inter.author.roles]
        if utils.StaffRoles.owner in _author_roles_ids or inter.author.id in self.bot.owner_ids:
            staff_rank = 'Owner'
        elif utils.StaffRoles.admin in _author_roles_ids:
            staff_rank = 'Admin'
        elif utils.StaffRoles.mod in _author_roles_ids:
            staff_rank = 'Moderator'

        if utils.StaffRoles.owner in (r.id for r in member.roles):  # Checks for owner
            entry.is_owner = True
        elif utils.StaffRoles.admin in (r.id for r in member.roles):  # Checks for admin
            entry.is_admin = True
        elif utils.StaffRoles.mod in (r.id for r in member.roles):  # Checks for mod
            entry.is_mod = True

        guild = self.bot.get_guild(1116770122770685982)
        muted_role = guild.get_role(utils.ExtraRoles.muted)
        new_roles = [r for r in member.roles if r.id not in utils.StaffRoles.all] + [muted_role]
        await member.edit(roles=new_roles, reason=f'Muted by: {inter.author.display_name} ({inter.author.id})')

        em = disnake.Embed()
        em.title = f'You have been muted in `{guild.name}`'
        em.add_field(
            'Reason',
            time_and_reason.arg,
            inline=False
        )
        em.add_field(
            'Duration',
            mute_duration,
            inline=False
        )
        em.add_field(
            'Expires On',
            expiration_date,
            inline=False
        )
        em.add_field(
            'Muted By',
            inter.author.display_name + f' (**{staff_rank}**)',
            inline=False
        )
        em.color = utils.red

        await utils.try_dm(member, embed=em)
        await inter.send(
            f'> 👌 📨 {member.mention} has been muted until {expiration_date} (`{mute_duration}`)'
        )

        entry.muted_until = time_and_reason.dt
        entry.duration = mute_duration
        entry.reason = reason
        entry.is_muted = True

        if had_entry is True:
            await entry.commit()
        else:
            await self.bot.db.add('mutes', entry)

        await utils.log(
            self.bot.webhooks['mod_logs'],
            title=f'[Mute]',
            fields=[
                ('Member', f'{member.display_name} (`{member.id}`)'),
                ('Reason', reason),
                ('Duration', mute_duration),
                ('Expires At', expiration_date),
                ('By', f'{inter.author.mention} (`{inter.author.id}`)'),
                ('At', utils.format_dt(datetime.now(), 'F')),
            ]
        )

    @commands.slash_command(name='unmute')
    async def unmute(self, inter: disnake.AppCmdInter, member: disnake.Member):
        """Unmutes a member."""

        if await self.check_perms(inter) is False:
            return
        
        entry: utils.Mute = await self.bot.db.get('mutes', member.id)
        if entry is None or entry.is_muted is False:
            return await inter.send(f'{self.bot.denial} That member is not muted!', ephemeral=True)

        guild = self.bot.get_guild(1116770122770685982)
        _muted_by = guild.get_member(entry.muted_by)
        new_roles = [r for r in member.roles if r.id != utils.ExtraRoles.muted]
        if entry.is_owner is True:
            new_roles += [guild.get_role(utils.StaffRoles.owner)]
        if entry.is_admin is True:
            new_roles += [guild.get_role(utils.StaffRoles.admin)]
        if entry.is_mod is True:
            new_roles += [guild.get_role(utils.StaffRoles.mod)]

        await member.edit(roles=new_roles, reason=f'Unmuted by: {inter.author.display_name} ({inter.author.id})')

        staff_rank = 'Apparently not a staff member, please contact the owner about this issue.'
        _author_roles_ids = [r.id for r in inter.author.roles]
        if utils.StaffRoles.owner in _author_roles_ids or inter.author.id in self.bot.owner_ids:
            staff_rank = 'Owner'
        elif utils.StaffRoles.admin in _author_roles_ids:
            staff_rank = 'Admin'
        elif utils.StaffRoles.mod in _author_roles_ids:
            staff_rank = 'Moderator'

        if entry.filter is True:
            if entry.streak == 7:
                await self.bot.db.delete('mutes', {'_id': entry.pk})
            else:
                entry.streak_expire_date = datetime.now() + relativedelta(days=21)
                entry.is_muted = False
                await entry.commit()

            muted_by = 'Automod'
        else:
            if entry.streak == 0:
                await self.bot.db.delete('mutes', {'_id': entry.pk})
            else:
                entry.is_muted = False
                await entry.commit()

            muted_by_staff_rank = 'Apparently not a staff member, please contact the owner about this issue.'
            _muted_by_roles_ids = [r.id for r in _muted_by.roles]
            if utils.StaffRoles.owner in _muted_by_roles_ids or _muted_by.id in self.bot.owner_ids:
                muted_by_staff_rank = 'Owner'
            elif utils.StaffRoles.admin in _muted_by_roles_ids:
                muted_by_staff_rank = 'Admin'
            elif utils.StaffRoles.mod in _muted_by_roles_ids:
                muted_by_staff_rank = 'Moderator'
            muted_by = f'{_muted_by.display_name} (**{muted_by_staff_rank}**)'

        if entry.permanent is True:
            mute_duration = 'PERMANENT'
            expiration_date = 'PERMANENT'
            remaining = 'PERMANENT'
        else:
            mute_duration = entry.duration
            expiration_date = utils.format_dt(entry.muted_until, 'F')
            remaining = utils.human_timedelta(entry.muted_until, suffix=False)

        em = disnake.Embed()
        em.title = f'You have been unmuted in `{guild.name}`'
        em.add_field(
            'Unmuted By',
            inter.author.display_name + f' (**{staff_rank}**)',
            inline=False
        )
        em.add_field(
            'Original Reason',
            entry.reason,
            inline=False
        )
        em.add_field(
            'Original Duration',
            mute_duration,
            inline=False
        )
        em.add_field(
            'Original Expiration date',
            expiration_date,
            inline=False
        )
        em.add_field(
            'Time Remaining',
            remaining,
            inline=False
        )
        em.add_field(
            'Originally Muted By',
            muted_by,
            inline=False
        )
        em.color = utils.green

        await utils.try_dm(member, embed=em)
        await inter.send(
            f'> 👌 {member.mention} has been unmuted.'
        )

        await utils.log(
            self.bot.webhooks['mod_logs'],
            title=f'[UNMUTE]',
            fields=[
                ('Member', f'{member.display_name} (`{member.id}`)'),
                ('Original Reason', entry.reason)
                ('Original Duration', f'`{mute_duration}`'),
                ('Original Expiration Date', f'`{expiration_date}`'),
                ('Remaining', f'`{remaining}`'),
                ('Originally Muted By', f'`{_muted_by.mention}` (`{_muted_by.id}`)'),
                ('By', f'{inter.author.mention} (`{inter.author.id}`)'),
                ('At', utils.format_dt(datetime.now(), 'F')),
            ]
        )

    @tasks.loop(seconds=5.0)
    async def check_mutes(self):
        entries: list[utils.Mute] = await self.bot.db.find_sorted('mutes', 'muted_until', 1, {'is_muted': True})
        for entry in entries[:15]:
            if datetime.now(entry.muted_until.tzinfo) >= entry.muted_until:
                guild = self.bot.get_guild(1116770122770685982)
                member = guild.get_member(entry.id)
                _mem = f'**[LEFT]** (`{entry.id}`)'

                if member:
                    _mem = f'{member.display_name} (`{member.id}`)'
                    new_roles = [role for role in member.roles if role.id != utils.ExtraRoles.muted]
                    if entry.is_owner is True:
                        owner_role = guild.get_role(utils.StaffRoles.owner)  # Check for owner
                        new_roles += [owner_role]
                    elif entry.is_admin is True:
                        admin_role = guild.get_role(utils.StaffRoles.admin)  # Check for admin
                        new_roles += [admin_role]
                    elif entry.is_mod is True:
                        mod_role = guild.get_role(utils.StaffRoles.mod)  # Check for mod
                        new_roles += [mod_role]
                    await member.edit(roles=new_roles, reason=f'[UNMUTE] Mute Expired.')
                    await utils.try_dm(
                        member,
                        f'Hello, your mute in `{guild.name}` has expired. You have been unmuted.'
                    )

                if entry.filter is True:
                    entry.is_muted = False
                    entry.streak_expire_date = datetime.now() + relativedelta(days=21)
                    await entry.commit()
                else:
                    if entry.streak == 0:
                        await self.bot.db.delete('mutes', {'_id': entry.id})
                    else:
                        entry.is_muted = False
                        await entry.commit()

                mem = guild.get_member(entry.muted_by)
                await utils.log(
                    self.bot.webhooks['mod_logs'],
                    title='[MUTE EXPIRED]',
                    fields=[
                        ('Member', _mem),
                        ('Reason', entry.reason),
                        ('Mute Duration', f'`{entry.duration}`'),
                        ('By', mem.mention),
                        ('At', utils.format_dt(datetime.now(), 'F')),
                    ]
                )

    @check_mutes.before_loop
    async def mutes_wait_until_ready(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=5.0)
    async def check_streaks(self):
        entries: list[utils.Mute] = await self.bot.db.find_sorted('mutes', 'streak_expire_date', 1, {'is_muted': False})
        for entry in entries[:10]:
            if datetime.now() >= entry.streak_expire_date:
                await self.bot.db.delete('mutes', {'_id': entry.pk})

                guild = self.bot.get_guild(1116770122770685982)
                usr = guild.get_member(entry.id)
                if usr:
                    mem = f'{usr.display_name} (`{usr.id}`)'
                else:
                    mem = f'**[LEFT]** (`{entry.id}`)'

                await utils.log(
                    self.bot.webhooks['mod_logs'],
                    title='[STREAK RESET]',
                    fields=[
                        ('User', mem),
                        ('At', utils.format_dt(datetime.now(), 'F')),
                    ]
                )

    @check_streaks.before_loop
    async def streaks_wait_until_ready(self):
        await self.bot.wait_until_ready()


def setup(bot: Askro):
    bot.add_cog(Moderation(bot))