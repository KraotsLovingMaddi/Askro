from datetime import datetime
from dateutil.relativedelta import relativedelta

import disnake
from disnake.ext import commands

import utils

from main import Askro


class Moderation(commands.Cog):
    """Staff related commands."""
    def __init__(self, bot: Askro):
        self.bot = bot

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
        await member.edit(roles=new_roles, reason=f'Muted by {inter.author.display_name}')

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


def setup(bot: Askro):
    bot.add_cog(Moderation(bot))