import disnake

AGE_ROLES = {
    '14': 1123496473544376320, '15': 1123496474823635017, '16': 1123496476090318911,
    '17': 1123496477738684526, '18': 1123496479202480168, '19': 1123496479202480168
}


class AgeButtonRoles(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='14', custom_id='askro:age_roles:14', row=0, style=disnake.ButtonStyle.blurple)
    async def _14(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Age role update.')
        await interaction.response.send_message(
            f'I have changed your age role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='15', custom_id='askro:age_roles:15', row=0, style=disnake.ButtonStyle.blurple)
    async def _15(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Age role update.')
        await interaction.response.send_message(
            f'I have changed your age role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='16', custom_id='askro:age_roles:16', row=0, style=disnake.ButtonStyle.blurple)
    async def _16(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Age role update.')
        await interaction.response.send_message(
            f'I have changed your age role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='17', custom_id='askro:age_roles:17', row=1, style=disnake.ButtonStyle.blurple)
    async def _17(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Age role update.')
        await interaction.response.send_message(
            f'I have changed your age role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='18', custom_id='askro:age_roles:18', row=1, style=disnake.ButtonStyle.blurple)
    async def _18(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Age role update.')
        await interaction.response.send_message(
            f'I have changed your age role to `{button.label}`', 
            phemeral=True
        )

    @disnake.ui.button(label='19', custom_id='askro:age_roles:19', row=1, style=disnake.ButtonStyle.blurple)
    async def _19(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        roles = [role for role in interaction.author.roles if role.id not in AGE_ROLES.values()]
        roles.append(interaction.guild.get_role(AGE_ROLES[button.label]))
        await interaction.author.edit(roles=roles, reason='Age role update.')
        await interaction.response.send_message(
            f'I have changed your age role to `{button.label}`', 
            phemeral=True
        )
