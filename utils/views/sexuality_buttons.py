
import disnake

SEXUALITY_ROLES = {
    'Straight': 1123495958756474890, 'Bisexual': 1123495959872143400, 'Gay': 1123495960992030751,
    'Lesbian': 1123495962506178621, 'Pansexual': 1123495964645281873, 'Asexual': 1123495969795866655,
    'Other Sexuality': 1123495972119519273
}


class SexualityButtonRoles(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Straight', custom_id='askro:sexuality_roles:Straight', row=0, style=disnake.ButtonStyle.blurple)
    async def Straight(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Bisexual', custom_id='askro:sexuality_roles:Bisexual', row=0, style=disnake.ButtonStyle.blurple)
    async def Bisexual(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Gay', custom_id='askro:sexuality_roles:Gay', row=0, style=disnake.ButtonStyle.blurple)
    async def Gay(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Lesbian', custom_id='askro:sexuality_roles:Lesbian', row=1, style=disnake.ButtonStyle.blurple)
    async def Lesbian(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Pansexual', custom_id='askro:sexuality_roles:Pansexual', row=1, style=disnake.ButtonStyle.blurple)
    async def Pansexual(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Asexual', custom_id='askro:sexuality_roles:Asexual', row=1, style=disnake.ButtonStyle.blurple)
    async def Asexual(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Other Sexuality', custom_id='askro:sexuality_roles:OtherSexuality', row=2, style=disnake.ButtonStyle.blurple)
    async def Other_Sexuality(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in SEXUALITY_ROLES.values()]
        roles.append(interaction.guild.get_role(SEXUALITY_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Sexuality role update.')
        await interaction.response.send_message(
            f'I have changed your sexuality role to `{button.label}`', 
            phemeral=True
        )
