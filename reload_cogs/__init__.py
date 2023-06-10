import os

import disnake
from disnake.ext import commands

import utils
from utils.context import Context

from main import Askro


class Cogs(commands.Cog):
    """Commands to reload cogs."""

    def __init__(self, bot: Askro):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True, hidden=True)
    @commands.is_owner()
    async def load(self, ctx: Context, extension):
        self.bot.load_extension(extension)
        await ctx.reply(f":inbox_tray: `{extension}`")

    @commands.group(name='reload', invoke_without_command=True, case_insensitive=True, hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx: Context, extension):
        self.bot.unload_extension(extension)
        self.bot.load_extension(extension)
        await ctx.reply(f":repeat: `{extension}`")

    @commands.group(invoke_without_command=True, case_insensitive=True, hidden=True)
    @commands.is_owner()
    async def unload(self, ctx: Context, extension):
        self.bot.unload_extension(extension)
        await ctx.reply(f":outbox_tray: `{extension}`")

    @_reload.command(aliases=["all"], hidden=True)
    @commands.is_owner()
    async def reload_all(self, ctx: Context):
        cogs_list = []
        em = disnake.Embed(color=utils.invisible, title="Reloaded the next cogs:")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.unload_extension(f'cogs.{filename[:-3]}')
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
                    a = f":repeat: `cogs.{filename[:-3]}`\n"
                    cogs_list.append(a)

                    final_Cogs = "".join(cogs_list)
                except Exception:
                    b = f"❌ `cogs.{filename[:-3]}`\n"
                    cogs_list.append(b)

                    final_Cogs = "".join(cogs_list)

        em.description = final_Cogs
        em.set_footer(
            text="If the cog has an ❌, then it means it failed to load, or was never loaded."
        )
        await ctx.reply(embed=em)

    @load.command(aliases=["all"], hidden=True)
    @commands.is_owner()
    async def load_all(self, ctx: Context):
        cogs_list = []
        em = disnake.Embed(color=utils.invisible, title="Loaded the next cogs:")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
                    a = f":inbox_tray: `cogs.{filename[:-3]}`\n"
                    cogs_list.append(a)

                    final_Cogs = "".join(cogs_list)
                except Exception:
                    b = f"❌ `cogs.{filename[:-3]}`\n"
                    cogs_list.append(b)

                    final_Cogs = "".join(cogs_list)

        em.description = final_Cogs
        em.set_footer(
            text="If the cog has an ❌, then it means it failed to load, or was already loaded."
        )
        await ctx.reply(embed=em)

    @unload.command(aliases=["all"], hidden=True)
    @commands.is_owner()
    async def unload_all(self, ctx: Context):
        cogs_list = []
        em = disnake.Embed(color=utils.invisible, title="Unloaded the next cogs:")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.unload_extension(f'cogs.{filename[:-3]}')
                    a = f":outbox_tray: `cogs.{filename[:-3]}`\n"
                    cogs_list.append(a)

                    final_Cogs = "".join(cogs_list)
                except Exception:
                    b = f"❌ `cogs.{filename[:-3]}`\n"
                    cogs_list.append(b)

                    final_Cogs = "".join(cogs_list)

        em.description = final_Cogs
        em.set_footer(
            text="If the cog has an ❌, then it means it failed to unload, or was never loaded."
        )
        await ctx.reply(embed=em)


def setup(bot: Askro):
    bot.add_cog(Cogs(bot))