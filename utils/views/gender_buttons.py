import disnake

GENDER_ROLES = {
    'Cis Male': 1123495932667895930, 'Cis Female': 1123495943711498280, 'Trans Female': 1123495945640886386,
    'Trans Male': 1123495946756575324, 'Non Binary': 1123495949176676452, 'Other Gender': 1123495951026372648
}


class GenderButtonRoles(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Cis Male', custom_id='askro:gender_roles:Male', row=0, style=disnake.ButtonStyle.blurple)
    async def Cis_Male(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Gender role update.')
        await interaction.response.send_message(
            f'I have changed your gender role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Cis Female', custom_id='askro:gender_roles:Female', row=0, style=disnake.ButtonStyle.blurple)
    async def Cis_Female(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Gender role update.')
        await interaction.response.send_message(
            f'I have changed your gender role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Trans Male', custom_id='askro:gender_roles:TransMale', row=0, style=disnake.ButtonStyle.blurple)
    async def Trans_Male(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Gender role update.')
        await interaction.response.send_message(
            f'I have changed your gender role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Trans Female', custom_id='askro:gender_roles:TransFemale', row=1, style=disnake.ButtonStyle.blurple)
    async def Trans_Female(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Gender role update.')
        await interaction.response.send_message(
            f'I have changed your gender role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Non Binary', custom_id='askro:gender_roles:NonBinary', row=1, style=disnake.ButtonStyle.blurple)
    async def Non_Binary(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Gender role update.')
        await interaction.response.send_message(
            f'I have changed your gender role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='Other Gender', custom_id='askro:gender_roles:OtherGender', row=1, style=disnake.ButtonStyle.blurple)
    async def Other_Gender(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in GENDER_ROLES.values()]
        roles.append(interaction.guild.get_role(GENDER_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Gender role update.')
        await interaction.response.send_message(
            f'I have changed your gender role to `{button.label}`', 
            phemeral=True
        )
