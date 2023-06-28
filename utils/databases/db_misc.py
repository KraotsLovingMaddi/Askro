from . import misc_database, GetDoc

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(misc_database)


@instance.register
class Misc(Document, GetDoc):
    """This is really just meant to store random stuff, enabled/disabled stuff or values."""

    id = IntField(attribute='_id', default=1116768380402270239)
    disabled_commands = ListField(StrField(), default=[])
    min_account_age = IntField(default=7)
    bad_words = DictField(StrField(), IntField())
    rules = ListField(StrField())
    in_lockdown = BoolField(default=False)

    class Meta:
        collection_name = 'Miscellaneous'