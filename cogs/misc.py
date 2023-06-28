import disnake
from disnake.ext import commands

import utils

from main import Askro


class Misc(commands.Cog):
    """Miscellaneous commands, basically commands that i have no fucking idea where to fucking put so they just come in this category."""
    def __init__(self, bot: Askro):
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return '🔧'

    @commands.slash_command(name='rules')
    async def rules(self, inter):
        pass

    @rules.sub_command(name='view')
    async def rules_view(self, inter: disnake.AppCmdInter, rule: int = None):
        """Sends the server's rules. If ``rule`` is given, it will only send that rule."""

        entry: utils.Misc = await self.bot.db.get('misc')
        if entry.rules is None:
            return await inter.send(
                f'{self.bot.denial} There are currently no rules set. Please contact an admin about this!',
                ephemeral=True
            )
        embeds = []

        if rule is None:
            em = disnake.Embed(title='Rules', color=utils.blurple)
            em.set_footer(text='NOTE: Breaking any of these rules will result in a mute, or in the worst case, a ban.')
            for index, rule in enumerate(entry.rules):
                if index in (10, 20, 30, 40, 50):  # Show 10 rules per embed
                    embeds.append(em)
                    em = disnake.Embed(title='Rules', color=utils.blurple)
                    em.set_footer(text='NOTE: Breaking any of these rules will result in a mute, or in the worst case, a ban.')

                if em.description is None:
                    em.description = f'`{index + 1}.` {rule}'
                else:
                    em.description += f'\n\n`{index + 1}.` {rule}'
            embeds.append(em)

        else:
            em = disnake.Embed(title='Rules', color=utils.blurple)
            if rule <= 0:
                return await inter.send(
                    f'{self.bot.denial} Rule cannot be equal or less than `0`',
                    ephemeral=True
                )
            try:
                _rule = entry.rules[rule - 1]
                em.description = f'`{rule}.` {_rule}'
            except IndexError:
                return await inter.send(f'{self.bot.denial} Rule does not exist!', ephemeral=True)
            em.set_footer(text='NOTE: Breaking any of these rules will result in a mute, or in the worst case, a ban.')
            embeds.append(em)

        await inter.send(embeds=embeds)

    @rules.sub_command(name='add')
    async def rules_add(self, inter: disnake.AppCmdInter, rule: str):
        """Adds a rule to the server's rules."""

        if not any(r for r in (utils.StaffRoles.owner, utils.StaffRoles.admin) if r in (role.id for role in inter.author.roles)):
            if inter.author.id not in self.bot.owner_ids:
                await inter.send(
                    f'{self.bot.denial} This command can only be used by admins and above!',
                    ephemeral=True
                )

        entry: utils.Misc = await self.bot.db.get('misc')
        if entry.rules is None:
            entry.rules = [rule]
        else:
            entry.rules += [rule]
            await entry.commit()

        await inter.send(f'> 👌 📝 `{utils.escape_markdown(rule)}` successfully **added** to the rules.')

    @rules.sub_command(name='edit')
    async def server_rules_edit(self, inter: disnake.AppCmdInter, rule: int, new_rule: str):
        """Edits an existing rule."""

        if not any(r for r in (utils.StaffRoles.owner, utils.StaffRoles.admin) if r in (role.id for role in inter.author.roles)):
            if inter.author.id not in self.bot.owner_ids:
                await inter.send(
                    f'{self.bot.denial} This command can only be used by admins and above!',
                    ephemeral=True
                )

        entry: utils.Misc = await self.bot.db.get('misc')
        if entry.rules is None:
            return await inter.send(
                f'{self.bot.denial} There are currently no rules set.',
                ephemeral=True
            )
        elif rule == 0:
            return await inter.send(
                f'{self.bot.denial} Rule cannot be ``0``',
                ephemeral=True
            )

        rule -= 1
        try:
            entry.rules[rule] = new_rule
        except IndexError:
            return await inter.send(
                f'{self.bot.denial} Rule does not exist!',
                ephemeral=True
            )
        await entry.commit()

        await inter.send(f'> 👌 📝 Successfully **edited** rule `{rule + 1}` to `{new_rule}`.')

    @rules.sub_command(name='remove')
    async def server_rules_remove(self, inter: disnake.AppCmdInter, rule: int):
        """Removes a rule from the server's rules by its number."""

        if not any(r for r in (utils.StaffRoles.owner, utils.StaffRoles.admin) if r in (role.id for role in inter.author.roles)):
            if inter.author.id not in self.bot.owner_ids:
                await inter.send(
                    f'{self.bot.denial} This command can only be used by admins and above!',
                    ephemeral=True
                )

        entry: utils.Misc = await self.bot.db.get('misc')
        if entry.rules is None:
            return await inter.send(
                f'{self.bot.denial} There are currently no rules set.',
                ephemeral=True
            )
        else:
            if rule <= 0:
                return await inter.send(
                    f'{self.bot.denial} Rule cannot be equal or less than `0`',
                    ephemeral=True
                )
            try:
                entry.rules.pop(rule - 1)
            except IndexError:
                return await inter.send(
                    f'{self.bot.denial} Rule does not exist!',
                    ephemeral=True
                )
            await entry.commit()

        await inter.send(f'> 👌 Successfully **removed** rule `{rule}`.')

    @rules.sub_command(name='clear')
    async def server_rules_clear(self, inter: disnake.AppCmdInter):
        """Deletes all the rules."""

        if not any(r for r in (utils.StaffRoles.owner,) if r in (role.id for role in inter.author.roles)):
            if inter.author.id not in self.bot.owner_ids:
                await inter.send(
                    f'{self.bot.denial} This command can only be used by owners!',
                    ephemeral=True
                )

        entry: utils.Misc = await self.bot.db.get('misc')
        if entry.rules is None:
            return await inter.send(
                f'{self.bot.denial} There are currently no rules set.',
                ephemeral=True
            )
        else:
            entry.rules = None
            await entry.commit()

        await inter.send('> 👌 Successfully **cleared** the rules.')


def setup(bot: Askro):
    bot.add_cog(Misc(bot))