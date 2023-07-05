import disnake

from utils import Context

ALL_COLOURS = {
    'Romantic Red': 1122943489588613170, 'Orange': 1122943590293839944, 'Yummy Yellow': 1122943776655155230,
    'Gorgeous Green': 1122943868145508526, 'Bold Blue': 1122943930472878100, 'Princess Purple': 1122943995211956375,
    'Petty Pink': 1122944070579396718, 'Terrific Turquoise': 1122944143019216916, 'Puffy Paint Purple': 1122944329758031993,
    'Grassy Green': 1122945000964096184, 'Sandy Orange': 1122945252450381824, 'Black Sharpie': 1122945429286420560,
    'Clean White Teeth': 1122945621301661800, 'Peachy Pink': 1122946182721851564, 'Lightning Lime': 1122946618568736819,
    'Lustful Lavender': 1122946813985574994, 'Rosey Red': 1122946925268844564, 'Coffee Bean Brown': 1122947335916367954,
    'Grimey Grey': 1122947457345662998
}

COLOURS_EMOJIS = {
    'Romantic Red': '<:romantic_red:1122966159990472815>', 'Orange': '<:orange:1122966149777338610>',
    'Yummy Yellow': '<:yummy_yellow:1122966168773341366>', 'Gorgeous Green': '<:gorgeous_green:1122966139811663892>',
    'Bold Blue': '<:bold_blue:1122966134275182713>', 'Princess Purple': '<:princess_purple:1122966515638083684>',
    'Petty Pink': '<:petty_pink:1122966153975828541>', 'Terrific Turquoise': '<:terrific_turquoise:1122966165715681282>',
    'Puffy Paint Purple': '<:puffy_paint_purple:1122966156765049083>', 'Grassy Green': '<:grassy_green:1122966141514559600>',
    'Sandy Orange': '<:sandy_orange:1122966546512367647>', 'Black Sharpie': '<:black_sharpie:1122966131439837296>',
    'Clean White Teeth': '<:clean_white_teeth:1122966135776755875>', 'Peachy Pink': '<:peachy_pink:1122966152495251566>',
    'Lightning Lime': '<:lightning_lime:1122966145511735346>', 'Lustful Lavender': '<:lustful_lavender:1122966148078649568>',
    'Rosey Red': '<:rosey_red:1122966535066099834>', 'Coffee Bean Brown': '<:coffee_bean_brown:1122966137332846643>',
    'Grimey Grey': '<:grimey_grey:1122966143548784671>'
}


class ColourButtonItem(disnake.ui.Button):
    def __init__(self, label, emoji):
        super().__init__(
            label=label,
            emoji=emoji,
            custom_id=f'askro:colours:{label.replace(" ", "")}'
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in ALL_COLOURS.values()]
        roles.append(interaction.guild.get_role(ALL_COLOURS[self.label]))
        await interaction.author.edit(roles=roles, reason='Colour role update via buttons.')
        await interaction.send(f'I have changed your colour to `{self.label}`', ephemeral=True)


class ColoursButtonRoles(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for colour_name in ALL_COLOURS.keys():
            self.add_item(ColourButtonItem(colour_name, COLOURS_EMOJIS[colour_name]))

    async def start_new_views(self, ctx: Context, message: str):
        self.clear_items()

        # Since we only have 19 colours that means we can just iterate over
        # in a range of 5 each time increasing the index with 4 so that next
        # iteration it takes from the next colour and the 4 next and so on.
        index = 0
        for _ in range(5):
            for colour_name in list(ALL_COLOURS.keys())[index:index + 4]:
                self.add_item(ColourButtonItem(colour_name, COLOURS_EMOJIS[colour_name]))

            index += 4
            await ctx.send(message, view=self)
            self.clear_items()