
import disnake

PRONOUNS_ROLES = {
    'He/Him': 1123495951793918095, 'She/Her': 1123495953249337374, 'They/Them': 1123495954335662213,
    'He/They': 1123495955682050079, 'She/They': 1123495956906770456
}


class PronounsButtonRoles(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='He/Him', custom_id='askro:pronouns_roles:HeHim', row=0, style=disnake.ButtonStyle.blurple)
    async def He_Him(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in PRONOUNS_ROLES.values()]
        roles.append(interaction.guild.get_role(PRONOUNS_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Pronouns role update.')
        await interaction.response.send_message(
            f'I have changed your pronouns role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='She/They', custom_id='askro:pronouns_roles:SheThey', row=0, style=disnake.ButtonStyle.blurple)
    async def She_They(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in PRONOUNS_ROLES.values()]
        roles.append(interaction.guild.get_role(PRONOUNS_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Pronouns role update.')
        await interaction.response.send_message(
            f'I have changed your pronouns role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='They/Them', custom_id='askro:pronouns_roles:TheyThem', row=0, style=disnake.ButtonStyle.blurple)
    async def They_Them(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in PRONOUNS_ROLES.values()]
        roles.append(interaction.guild.get_role(PRONOUNS_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Pronouns role update.')
        await interaction.response.send_message(
            f'I have changed your pronouns role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='He/They', custom_id='askro:pronouns_roles:HeThey', row=1, style=disnake.ButtonStyle.blurple)
    async def He_They(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in PRONOUNS_ROLES.values()]
        roles.append(interaction.guild.get_role(PRONOUNS_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Pronouns role update.')
        await interaction.response.send_message(
            f'I have changed your pronouns role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='She/They', custom_id='askro:pronouns_roles:SheThey', row=1, style=disnake.ButtonStyle.blurple)
    async def She_They(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in PRONOUNS_ROLES.values()]
        roles.append(interaction.guild.get_role(PRONOUNS_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Pronouns role update.')
        await interaction.response.send_message(
            f'I have changed your pronouns role to `{button.label}`', 
            phemeral=True
        )
