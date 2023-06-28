import disnake
from disnake.ext import commands
from disnake.interactions import MessageInteraction

from main import Askro

DMS_ROLES = {
    'DMS: Open': 1123496491445665792, 'DMS: Ask': 1123496493446344716, 'DMS: Closed': 1123496495224721440
}
AGE_ROLES = {
    '14': 1123496473544376320, '15': 1123496474823635017, '16': 1123496476090318911,
    '17': 1123496477738684526, '18': 1123496479202480168, '19': 1123496479202480168
}
GENDER_ROLES = {
    'Male': 1123495932667895930, 'Female': 1123495943711498280, 'Trans Female': 1123495945640886386,
    'Trans Male': 1123495946756575324, 'Non Binary': 1123495949176676452, 'Other Gender': 1123495951026372648
}
SEXUALITY_ROLES = {
    'Straight': 1123495958756474890, 'Bisexual': 1123495959872143400, 'Gay': 1123495960992030751,
    'Lesbian': 1123495962506178621, 'Pansexual': 1123495964645281873, 'Asexual': 1123495969795866655,
    'Other Sexuality': 1123495972119519273
}
PRONOUNS_ROLES = {
    'He/Him': 1123495951793918095, 'She/Her': 1123495953249337374, 'They/Them': 1123495954335662213,
    'He/They': 1123495955682050079, 'She/They': 1123495956906770456
}


class RolesDMSSelect(disnake.ui.Select['RolesView']):
    def __init__(self):
        super().__init__(placeholder='Select your DMS status...')
        self.__fill_options()

    def __fill_options(self):
        for value in DMS_ROLES.keys():
            self.add_option(label=value)

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        roles = [role for role in interaction.author.roles if role.id not in DMS_ROLES.values()]
        roles.append(interaction.guild.get_role(DMS_ROLES[value]))
        await interaction.author.edit(roles=roles, reason='DMS role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your DMS role to `{value}`')


class RolesAgeSelect(disnake.ui.Select['RolesView']):
    def __init__(self):
        super().__init__(placeholder='Select your age...')
        self.__fill_options()

    def __fill_options(self):
        for value in AGE_ROLES.keys():
            self.add_option(label=value)

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[value]))
        await interaction.author.edit(roles=roles, reason='Age role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your age role to `{value}`')


class RolesGenderSelect(disnake.ui.Select['RolesView']):
    def __init__(self):
        super().__init__(placeholder='Select your gender...')
        self.__fill_options()

    def __fill_options(self):
        for value in GENDER_ROLES.keys():
            self.add_option(label=value)

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[value]))
        await interaction.author.edit(roles=roles, reason='Gender role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your gender role to `{value}`')


class RolesSexualitySelect(disnake.ui.Select['RolesView']):
    def __init__(self):
        super().__init__(placeholder='Select your sexuality...')
        self.__fill_options()

    def __fill_options(self):
        for value in SEXUALITY_ROLES.keys():
            self.add_option(label=value)

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[value]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your sexuality role to `{value}`')


class RolesPronounsSelect(disnake.ui.Select['RolesView']):
    def __init__(self):
        super().__init__(placeholder='Select your pronouns...')
        self.__fill_options()

    def __fill_options(self):
        for value in PRONOUNS_ROLES.keys():
            self.add_option(label=value)

    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        value = self.values[0]
        roles = [role for role in interaction.author.roles if role.id not in PRONOUNS_ROLES.values()]
        roles.append(interaction.guild.get_role(PRONOUNS_ROLES[value]))
        await interaction.author.edit(roles=roles, reason='Pronouns role update via select menu.')
        await interaction.response.edit_message(content=f'Changed your pronouns role to `{value}`')


class RolesView(disnake.ui.View):
    def __init__(self, role_type: str):
        super().__init__(timeout=None)
        if role_type == 'DMS':
            self.add_item(RolesDMSSelect())
        elif role_type == 'Age':
            self.add_item(RolesAgeSelect())
        elif role_type == 'Gender':
            self.add_item(RolesGenderSelect())
        elif role_type == 'Sexuality':
            self.add_item(RolesSexualitySelect())
        elif role_type == 'Pronouns':
            self.add_item(RolesPronounsSelect())


class Roles(commands.Cog):
    def __init__(self, bot: Askro):
        self.bot = bot

    @commands.slash_command(name='roles')
    async def roles(
        self,
        inter: disnake.AppCmdInter,
        role_type: str = commands.Param(choices=[
            'DMS', 'Age', 'Gender',
            'Sexuality', 'Pronouns'
        ])
    ):
        """Change your roles."""

        await inter.send(
            f'Use the select menu below to change your `{role_type}`.',
            view=RolesView(role_type),
            ephemeral=True
        )


def setup(bot: Askro):
    bot.add_cog(Roles(bot))