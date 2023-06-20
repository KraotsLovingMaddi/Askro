from . import stories_database, GetDoc

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(stories_database)


@instance.register
class Story(Document, GetDoc):
    name = StrField(required=True)
    description = StrField(required=True)
    thumbnail = StrField()

    # {chapter_number: {story: ..., story_image: ...}}
    chapters = DictField(IntField(), DictField(StrField(), StrField()))
    characters = DictField(StrField(), StrField())

    written_by = IntField(required=True)

    # {fan_discord_id: {chapter_number: {story: ..., story_image: ...}}}
    fanfics = DictField(IntField(), DictField(IntField(), DictField(StrField(), StrField())))

    class Meta:
        collection_name = 'Stories'