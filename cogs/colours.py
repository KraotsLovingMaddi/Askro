import disnake
from disnake.ext import commands

from main import Askro


class ColoursSelect(disnake.ui.Select['ColoursView']):
    def __init__(self):
        super().__init__(placeholder='Select your colour...')
        self.__fill_options()

    def __fill_options(self):
        self.add_option(label='Romantic Red', emoji='<:romantic_red:1122966159990472815>')
        self.add_option(label='Orange', emoji='<:orange:1122966149777338610>')
        self.add_option(label='Yummy Yellow', emoji='<:yummy_yellow:1122966168773341366>')
        self.add_option(label='Gorgeous Green', emoji='<:gorgeous_green:1122966139811663892>')
        self.add_option(label='Bold Blue', emoji='<:bold_blue:1122966134275182713>')
        self.add_option(label='Princess Purple', emoji='<:princess_purple:1122966515638083684>')
        self.add_option(label='Petty Pink', emoji='<:petty_pink:1122966153975828541>')
        self.add_option(label='Terrific Turquoise', emoji='<:terrific_turquoise:1122966165715681282>')
        self.add_option(label='Puffy Paint Purple', emoji='<:puffy_paint_purple:1122966156765049083>')
        self.add_option(label='Grassy Green', emoji='<:grassy_green:1122966141514559600>')
        self.add_option(label='Sandy Orange', emoji='<:sandy_orange:1122966546512367647>')
        self.add_option(label='Black Sharpie', emoji='<:black_sharpie:1122966131439837296>')
        self.add_option(label='Clean White Teeth', emoji='<:clean_white_teeth:1122966135776755875>')
        self.add_option(label='Peachy Pink', emoji='<:peachy_pink:1122966152495251566>')
        self.add_option(label='Lightning Lime', emoji='<:lightning_lime:1122966145511735346>')
        self.add_option(label='Lustful Lavender', emoji='<:lustful_lavender:1122966148078649568>')
        self.add_option(label='Rosey Red', emoji='<:rosey_red:1122966535066099834>')
        self.add_option(label='Coffee Bean Brown', emoji='<:coffee_bean_brown:1122966137332846643>')
        self.add_option(label='Grimey Grey', emoji='<:grimey_grey:1122966143548784671>')

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        roles = [role for role in interaction.author.roles if role.id not in self.view.all_colours.values()]
        roles.append(interaction.guild.get_role(self.view.all_colours[value]))
        await interaction.author.edit(roles=roles, reason='Colour role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your colour to `{value}`')


class ColoursView(disnake.ui.View):
    all_colours = {
        'Romantic Red': 1122943489588613170, 'Orange': 1122943590293839944, 'Yummy Yellow': 1122943776655155230,
        'Gorgeous Green': 1122943868145508526, 'Bold Blue': 1122943930472878100, 'Princess Purple': 1122943995211956375,
        'Petty Pink': 1122944070579396718, 'Terrific Turquoise': 1122944143019216916, 'Puffy Paint Purple': 1122944329758031993,
        'Grassy Green': 1122945000964096184, 'Sandy Orange': 1122945252450381824, 'Black Sharpie': 1122945429286420560,
        'Clean White Teeth': 1122945621301661800, 'Peachy Pink': 1122946182721851564, 'Lightning Lime': 1122946618568736819,
        'Lustful Lavender': 1122946813985574994, 'Rosey Red': 1122946925268844564, 'Coffee Bean Brown': 1122947335916367954,
        'Grimey Grey': 1122947457345662998
    }

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ColoursSelect())


class Colours(commands.Cog):
    def __init__(self, bot: Askro):
        self.bot = bot

    @commands.slash_command(name='colours')
    async def colours(self, inter: disnake.AppCmdInter):
        """Change your colour."""

        await inter.send(
            'Use the select menu below to change your colour.',
            view=ColoursView(),
            ephemeral=True
        )


def setup(bot: Askro):
    bot.add_cog(Colours(bot))