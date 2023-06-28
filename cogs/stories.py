import disnake
from disnake.ext import commands

import utils
from utils import Story

from main import Askro


class StoryCreateModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label ='Name',
                custom_id ='story-create-name',
                placeholder='Type the name of your story...',
                style=disnake.TextInputStyle.short,
                max_length=100
            ),
            disnake.ui.TextInput(
                label ='Description',
                custom_id ='story-create-description',
                placeholder='Type a description of your story...',
                style=disnake.TextInputStyle.paragraph,
                max_length=750
            ),
            disnake.ui.TextInput(
                label ='Characters',
                custom_id ='story-create-characters',
                placeholder='Type some characters of your story separated by commas...',
                style=disnake.TextInputStyle.paragraph,
                max_length=1024
            ),
        ]
        super().__init__(
            title='Story Creation',
            components=components
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        fields = ['Name', 'Description', 'Characters']
        values = dict(zip(fields, interaction.text_values.values()))
        values['Characters'] = values['Characters'].split(',')

        story = await interaction.bot.db.find_one('stories', {'name': values['Name']})
        if story:
            author = interaction.bot.get_user(story.written_by)
            return await interaction.send(
                f'There already exists a story with the name {story.name} written by {author.mention}',
                ephemeral=True
            )

        await interaction.bot.db.add(
            'stories',
            Story(
                name=values['Name'],
                description=values['Description'],
                characters={k: '' for k in values['Characters']},
                written_by=interaction.author.id
            )
        )
        await interaction.send(f'Story {values["Name"]} successfully created.')


class StoryView(disnake.ui.View):
    def __init__(
        self,
        interaction: disnake.AppCmdInter,
        story: Story
    ):
        super().__init__()
        self.interaction = interaction
        self.story = story

    async def interaction_check(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.interaction.author.id and interaction.author.id not in self.interaction.bot.owner_ids:
            await interaction.response.send_message(
                f'Only **{self.interaction.author.display_name}** can use the buttons on this message!',
                ephemeral=True
            )
            return False
        return True

    async def on_error(self, error, item, inter):
        await self.bot.inter_reraise(inter, item, error)

    async def on_timeout(self):
        try:
            return await self.interaction.edit_original_message(view=None)
        except disnake.HTTPException:
            pass

    @disnake.ui.button(label='Original Story', style=disnake.ButtonStyle.blurple)
    async def original_story(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.send('You clicked `Original Story`', ephemeral=True)

    @disnake.ui.button(label='Fanfics', style=disnake.ButtonStyle.grey)
    async def fanfics(self, button: disnake.ui.Button, inter: disnake.Interaction):
        await inter.send('You clicked `Fanfics`', ephemeral=True)


class Stories(commands.Cog):
    def __init__(self, bot: Askro):
        self.bot = bot

    @commands.slash_command()
    async def story(self, inter):
        pass

    @story.sub_command(name='view')
    async def story_view(
        self,
        inter: disnake.AppCmdInter,
        story_name: str
    ):
        """View a story.

        Parameters
        ----------
        story_name: The name of the story you want to view.
        """

        if inter.author.id not in self.bot.owner_ids:
            return await inter.send('**[CURRENTLY UNDER DEVELOPMENT]**', ephemeral=True)

        story: Story = await self.bot.db.find_one('stories', {'name': story_name})
        if story is None:
            return await inter.send(f'No story named `{story_name}` found.', ephemeral=True)

        em = disnake.Embed()
        em.title = story.name
        em.description = story.description
        if story.thumbnail:
            em.set_image(url=story.thumbnail)

        guild = self.bot.get_guild(1116770122770685982)
        written_by = guild.get_member(story.written_by)
        # In case the user left, their story will be deleted anyways.
        written_by = written_by or self.bot.get_user(story.written_by)
        em.set_footer(text=f'Written by: {written_by}', icon_url=written_by.display_avatar)

        em.add_field(
            'Chapters',
            len(story.chapters) if story.chapters else 'No Chapters.'
        )
        em.add_field(
            'Fanfics',
            len(story.fanfics) if story.fanfics else 'No Fanfics.'
        )
        em.add_field(
            'Characters',
            len(story.characters) if story.characters else 'No Characters.'
        )

        await inter.send(embed=em, view=StoryView(inter, story))

    @story_view.autocomplete('story_name')
    async def story_view_autocomp(self, inter: disnake.AppCmdInter, user_input: str):
        names = [story_name for story_name in [story.name for story in await self.bot.db.find('stories')]]
        return utils.finder(user_input, names, lazy=False)[:25]

    @story.sub_command(name='create')
    async def story_create(
        self,
        inter: disnake.AppCmdInter
    ):
        """Create a story."""

        if inter.author.id not in self.bot.owner_ids:
            return await inter.send('**[CURRENTLY UNDER DEVELOPMENT]**', ephemeral=True)

        await inter.response.send_modal(StoryCreateModal())

def setup(bot: Askro):
    bot.add_cog(Stories(bot))