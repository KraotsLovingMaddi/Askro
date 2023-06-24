from datetime import datetime

import disnake
from disnake import TextInputStyle

from disnake.ui import Modal, TextInput
from disnake.ext import commands

import utils
from utils import Intros

from main import Askro


def create_intro_embed(intro: Intros, member: disnake.Member):
    em = disnake.Embed()
    em.set_author(
        name=member.display_name,
        url=member.display_avatar.url,
        icon_url=member.display_avatar.url
    )
    em.add_field(
        'Name',
        intro.name
    )
    em.add_field(
        'Age',
        intro.age
    )
    em.add_field(
        'Pronouns',
        intro.pronouns
    )
    em.add_field(
        'Gender',
        intro.gender
    )
    em.add_field(
        'Sexuality',
        intro.sexuality
    )
    em.add_field(
        '\u2800',
        '\u2800',
        inline=False
    )
    em.add_field(
        'Country',
        intro.country
    )
    em.add_field(
        'DMS',
        intro.dms
    )
    em.add_field(
        'Likes',
        intro.likes
    )
    em.add_field(
        'Dislikes',
        intro.dislikes
    )
    em.add_field(
        'Hobbies',
        intro.hobbies
    )
    em.set_footer(text='Intro created at')
    em.timestamp = intro.created_at
    em.set_thumbnail(url=member.display_avatar)
    
    return em


FIELDS = {
    'Name': {
        'label': 'Name',
        'custom_id': 'intro-name',
        'placeholder': 'Type here your name...',
        'style': TextInputStyle.short,
        'max_length': 100,
        'required': True
    },
    'Age': {
        'label': 'Age',
        'custom_id': 'intro-age',
        'placeholder': 'Type here your age...',
        'style': TextInputStyle.short,
        'max_length': 2,
        'required': True
    },
    'Pronouns': {
        'label': 'Pronouns',
        'custom_id': 'intro-pronouns',
        'placeholder': 'he/him, she/her, they/them, etc...',
        'style': TextInputStyle.short,
        'max_length': 30,
        'required': True
    },
    'Gender': {
        'label': 'Gender',
        'custom_id': 'intro-gender',
        'placeholder': 'male, female, trans male, trans female, etc...',
        'style': TextInputStyle.short,
        'max_length': 30,
        'required': True
    },
    'Sexuality': {
        'label': 'Sexuality',
        'custom_id': 'intro-sexuality',
        'placeholder': 'straight, bisexual, gay, lesbian, etc...',
        'style': TextInputStyle.short,
        'max_length': 30,
        'required': True
    },
    'Country': {
        'label': 'Country',
        'custom_id': 'intro-country',
        'placeholder': 'The country you live in...',
        'style': TextInputStyle.short,
        'max_length': 50,
        'required': True
    },
    'DMS': {
        'label': 'DMS',
        'custom_id': 'intro-dms',
        'placeholder': 'open/ask/closed...',
        'style': TextInputStyle.short,
        'max_length': 6,
        'required': True
    },
    'Likes': {
        'label': 'Likes',
        'custom_id': 'intro-likes',
        'placeholder': 'ice-cream, chocolate, etc...',
        'style': TextInputStyle.paragraph,
        'max_length': 1024,
        'required': True
    },
    'Dislikes': {
        'label': 'Dislikes',
        'custom_id': 'intro-dislikes',
        'placeholder': 'spiders, bugs, etc...',
        'style': TextInputStyle.paragraph,
        'max_length': 1024,
        'required': True
    },
    'Hobbies': {
        'label': 'Hobbies',
        'custom_id': 'intro-hobbies',
        'placeholder': 'Your hobbies...',
        'style': TextInputStyle.paragraph,
        'max_length': 1024,
        'required': True
    },
}


class IntroHalfOne(Modal):
    def __init__(self, inter, redoing: bool = False):
        components = [
            TextInput(
                **FIELDS['Name']
            ),
            TextInput(
                **FIELDS['Age']
            ),
            TextInput(
                **FIELDS['Pronouns']
            ),
            TextInput(
                **FIELDS['Gender']
            ),
            TextInput(
                **FIELDS['Sexuality']
            )
        ]
        super().__init__(title='Intro', components=components)
        self.inter = inter
        self.redoing = redoing

    async def callback(self, interaction: disnake.ModalInteraction):
        fields = ['Name', 'Age', 'Pronouns', 'Gender', 'Sexuality']
        values = dict(zip(fields, interaction.text_values.values()))

        try:
            values['Age'] = int(values['Age'])
        except ValueError:
            return await interaction.send(
                'The age must contain numbers from 0-9 and no letters or other characters..',
                ephemeral=True
            )
        
        if values['Age'] < 14 or values['Age'] > 19:
            if values['Age'] < 14:
                await utils.try_dm(
                    interaction.author,
                    '>>> <:disagree:938412299746689045> Sorry! You are too young for this server.'
                )
            elif values['Age'] > 19:
                await utils.try_dm(
                    interaction.author,
                    '>>> <:disagree:938412299746689045> Sorry! You are too old for this server.'
                )
            await interaction.author.ban(reason='User does not match age limits.')
            return await utils.log(
                interaction.bot.webhooks['mod_logs'],
                title='[BAN]',
                fields=[
                    ('Member', f'{interaction.author} (`{interaction.author.id}`)'),
                    ('Reason', f'User does not match age requirements. (`{values["Age"]} y/o`)'),
                    ('By', f'{interaction.bot.user.mention} (`{interaction.bot.user.id}`)'),
                    ('At', utils.format_dt(datetime.datetime.now(), 'F')),
                ]
            )

        if self.redoing is True:
            intro = await interaction.bot.db.get('intros', interaction.author.id)
            intro.name = values['Name']
            intro.age = values['Age']
            intro.pronouns = values['Pronouns']
            intro.gender = values['Gender']
            intro.sexuality = values['Sexuality']
        else:
            intro = Intros(
                id=interaction.author.id,
                name=values['Name'],
                age=values['Age'],
                pronouns=values['Pronouns'],
                gender=values['Gender'],
                sexuality=values['Sexuality']
            )

        await interaction.send(
            f'{interaction.author.mention} You are almost done. '
            'Press the button below to finish your intro.',
            view=ContinueIntro(intro, self.inter, self.redoing)
        )


class ContinueIntro(disnake.ui.View):
    def __init__(self, intro: Intros, inter, redoing: bool):
        super().__init__()
        self.intro: Intros = intro
        self.inter = inter
        self.redoing = redoing

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.inter.author.id and interaction.author.id not in self.inter.bot.owner_ids:
            await interaction.response.send_message(
                f'Only **{self.inter.author.display_name}** can use the buttons on this message!',
                ephemeral=True
            )
            return False
        return True

    async def on_error(self, error, item, inter):
        await self.inter.bot.inter_reraise(inter, item, error)

    async def on_timeout(self):
        try:
            return await self.inter.delete_original_response()
        except disnake.HTTPException:
            pass

    @disnake.ui.button(label='Continue', style=disnake.ButtonStyle.blurple)
    async def continue_intro(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(IntroHalfTwo(self.intro, self.redoing))
        await inter.delete_original_response()


class IntroHalfTwo(Modal):
    def __init__(self, intro: Intros, redoing: bool):
        components = [
            TextInput(
                **FIELDS['Country']
            ),
            TextInput(
                **FIELDS['DMS']
            ),
            TextInput(
                **FIELDS['Likes']
            ),
            TextInput(
                **FIELDS['Dislikes']
            ),
            TextInput(
                **FIELDS['Hobbies']
            )
        ]
        super().__init__(title='Intro', components=components)
        self.intro = intro
        self.redoing = redoing

    async def callback(self, interaction: disnake.ModalInteraction):
        fields = ['Country', 'DMS', 'Likes', 'Dislikes', 'Hobbies']
        values = dict(zip(fields, interaction.text_values.values()))

        if values['DMS'].lower() not in ('open', 'ask', 'closed'):
            return await interaction.send(
                'DMS must **only** be `open`, `ask`, or `closed`. Redo the intro and this time please only write one of those down.',
                ephemeral=True
            )

        self.intro.country = values['Country']
        self.intro.dms = values['DMS']
        self.intro.likes = values['Likes']
        self.intro.dislikes = values['Dislikes']
        self.intro.hobbies = values['Hobbies']

        channel = interaction.bot.get_guild(1116770122770685982).get_channel(utils.Channels.intros)
        em = create_intro_embed(self.intro, interaction.author)

        m = await channel.send(embed=em)
        self.intro.jump_url = m.jump_url

        if self.redoing is True:
            await utils.try_delete(message_id=self.intro.message_id, channel=channel)
            self.intro.message_id = m.id
            await self.intro.commit()
        else:
            self.intro.message_id = m.id
            await interaction.bot.db.add('intros', self.intro)

        await interaction.send(
            f'Intro finished. Check it out in {channel.mention}',
            view=utils.UrlButton('Jump!', self.intro.jump_url)
        )


class RedoIntro(disnake.ui.View):
    def __init__(self, inter):
        super().__init__()
        self.inter = inter

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.inter.author.id and interaction.author.id not in self.inter.bot.owner_ids:
            await interaction.response.send_message(
                f'Only **{self.inter.author.display_name}** can use the buttons on this message!',
                ephemeral=True
            )
            return False
        return True

    async def on_error(self, error, item, inter):
        await self.inter.bot.inter_reraise(inter, item, error)

    async def on_timeout(self):
        try:
            return await self.inter.delete_original_response()
        except disnake.HTTPException:
            pass

    @disnake.ui.button(label='Yes', style=disnake.ButtonStyle.green)
    async def redo_yes(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.send_modal(IntroHalfOne(self.inter, redoing=True))
        await inter.delete_original_response()

    @disnake.ui.button(label='No', style=disnake.ButtonStyle.red)
    async def redo_no(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.response.defer()
        await self.inter.delete_original_response()


class IntroEdit(Modal):
    def __init__(self, field: str):
        components = [
            TextInput(
                **FIELDS[field]
            )
        ]
        super().__init__(title='Intro Editing', components=components)
        self.field = field

    async def callback(self, interaction: disnake.ModalInteraction):
        value = interaction.text_values
        intro = await interaction.bot.db.get('intros', interaction.author.id)
        for k, v in value.items():
            if 'name' in k:
                intro.name = v
            if 'age' in k:
                intro.age = v
            if 'pronouns' in k:
                intro.pronouns = v
            if 'gender' in k:
                intro.gender = v
            if 'sexuality' in k:
                intro.sexuality = v
            if 'country' in k:
                intro.country = v
            if 'dms' in k:
                intro.dms = v
            if 'likes' in k:
                intro.likes = v
            if 'dislikes' in k:
                intro.dislikes = v
            if 'hobbies' in k:
                intro.hobbies = v

        try:
            intro.age = int(intro.age)
        except ValueError:
            return await interaction.send(
                'The age must contain numbers from 0-9 and no letters or other characters..',
                ephemeral=True
            )
        
        if intro.age < 14 or intro.age > 19:
            if intro.age < 14:
                await utils.try_dm(
                    interaction.author,
                    '>>> <:disagree:938412299746689045> Sorry! You are too young for this server.'
                )
            elif intro.age > 19:
                await utils.try_dm(
                    interaction.author,
                    '>>> <:disagree:938412299746689045> Sorry! You are too old for this server.'
                )
            await interaction.author.ban(reason='User does not match age limits.')
            return await utils.log(
                interaction.bot.webhooks['mod_logs'],
                title='[BAN]',
                fields=[
                    ('Member', f'{interaction.author} (`{interaction.author.id}`)'),
                    ('Reason', f'User does not match age requirements. (`{intro.age} y/o`)'),
                    ('By', f'{interaction.bot.user.mention} (`{interaction.bot.user.id}`)'),
                    ('At', utils.format_dt(datetime.datetime.now(), 'F')),
                ]
            )

        if intro.dms.lower() not in ('open', 'ask', 'closed'):
            return await interaction.send(
                'DMS must **only** be `open`, `ask`, or `closed`.',
                ephemeral=True
            )

        channel = interaction.bot.get_guild(1116770122770685982).get_channel(utils.Channels.intros)
        em = create_intro_embed(intro, interaction.author)

        m = await channel.send(embed=em)
        intro.jump_url = m.jump_url

        await utils.try_delete(message_id=intro.message_id, channel=channel)
        intro.message_id = m.id

        await intro.commit()
        await interaction.send(
            f'The field `{self.field}` in your intro has been updated. Check it out in {channel.mention}',
            view=utils.UrlButton('Jump!', intro.jump_url),
            ephemeral=True
        )


class Intro_(commands.Cog, name='Intros'):
    def __init__(self, bot: Askro):
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return '🙌'

    @commands.slash_command(name='intro', dm_permission=False)
    async def intro(self, inter):
        pass

    @intro.sub_command(name='create')
    async def intro_create(self, inter: disnake.AppCmdInter):
        """Use to create a new intro. Won't work if you already have one."""

        if await self.bot.db.get('intros', inter.author.id) is not None:
            return await inter.send(
                'You already have an intro. Do you wish to **redo** it?',
                view=RedoIntro(inter)
            )

        await inter.response.send_modal(IntroHalfOne(inter))

    @intro.sub_command(name='view')
    async def intro_view(
        self,
        inter: disnake.AppCmdInter,
        member: disnake.Member = commands.Param(lambda inter: inter.author)
    ):
        """Views a member's intro."""

        intro: Intros = await self.bot.db.get('intros', member.id)
        if intro is None:
            return await inter.send(
                '>>> <:disagree:938412299746689045> '
                f'{"You do not" if member.id == inter.author.id else str(member) + " does not"} '
                'have an intro.',
                ephemeral=True
            )

        em = create_intro_embed(intro, inter.author)

        await inter.send(embed=em, view=utils.UrlButton('Jump!', intro.jump_url))

    @intro.sub_command(name='edit')
    async def intro_edit(
        self,
        inter: disnake.AppCmdInter,
        field: str = commands.Param(choices=[
            'Name', 'Age', 'Pronouns', 'Gender', 'Sexuality',
            'Country', 'DMS', 'Likes', 'Dislikes', 'Hobbies'
        ])
    ):
        """Edit a field in your intro."""

        intro: Intros = await self.bot.db.get('intros', inter.author.id)
        if intro is None:
            return await inter.send(
                '>>> <:disagree:938412299746689045> You do not have an intro.',
                ephemeral=True
            )

        await inter.response.send_modal(IntroEdit(field))

    @commands.slash_command(name='unverify', dm_permission=False)
    async def unverify(self, inter: disnake.AppCmdInter, member: disnake.Member):
        """Unverifies a member if they have a troll or malicious intro."""

        if inter.author.id not in self.bot.owner_ids:
            if not any(r for r in (utils.StaffRoles.owner,) if r in (role.id for role in inter.author.roles)):
                return await inter.send(
                    '>>> <:disagree:938412299746689045> You are not allowed to use this command.',
                    ephemeral=True
                )
            # elif member.top_role >= inter.author.top_role:
            #     return await inter.send(
            #         '>>> <:disagree:938412299746689045> You can\'t unverify staff members of the same or higher rank than you.',
            #         ephemeral=True
            #     )

        intro: Intros = await self.bot.db.get('Intros', member.id)
        if intro is None:
            return await inter.send(
                f'>>> <:disagree:938412299746689045> {member.mention} does not have an intro.',
                ephemeral=True
            )

        await self.bot.db.delete('intros', {'_id': intro.id})
        guild = inter.bot.get_guild(1116770122770685982)
        unverified_role = guild.get_role(1121949200414949447)
        await member.edit(roles=[unverified_role])
        await utils.try_dm(
            member,
            f'Hello! You have been unverified in `{guild.name}`. '
            f'To verify again go to <#{utils.Channels.verify}> and type `/intro create`'
        )
        await inter.send(f'> <:agree:938412298769432586> Successfully unverified {member.mention}')

    @commands.Cog.listener('on_message')
    async def verify_on_message(self, message: disnake.Message):
        if message.channel.id == utils.Channels.verify and message.author.id != self.bot.user.id:
            await message.delete()

    @commands.Cog.listener('on_member_remove')
    async def intro_cleanup(self, member: disnake.Member):
        if member.guild.id == 1116770122770685982:
            await self.bot.db.delete('intros', {'_id': member.id})


def setup(bot: Askro):
    bot.add_cog(Intro_(bot))