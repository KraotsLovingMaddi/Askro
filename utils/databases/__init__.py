from .dbs import (
    levels_database,
    mutes_database,
    marriages_database,
    misc_database,
    stories_database,
    intros_database
)


class GetDoc:
    @classmethod
    async def get(cls, id=1116768380402270239):
        """|coro|

        This method is a shortcut for ``await .find_one({'_id': id})``
        If the ``id`` isn't given, then it will use the owner's id by default (1116768380402270239)
        """

        return await cls.find_one({'_id': id})
    

from .db_levels import Level
from .db_mutes import Mute
from .db_marriages import Marriage
from .db_misc import Misc
from .db_stories import Story
from .db_intros import Intros

__all__ = (
    'Level',
    'Mute',
    'Marriage',
    'Misc',
    'Story',
    'Intros'
)

from .objects import Database