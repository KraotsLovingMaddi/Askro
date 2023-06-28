from typing import NamedTuple

import string as st
from datetime import datetime

__all__ = (
    'FIRST_JANUARY_1970',
    'ALLOWED_CHARACTERS',
    'EDGE_CHARACTERS_CASES',
    'EDGE_CHARACTERS_TABLE',
    'PUNCTUATIONS_AND_DIGITS',
    'PAD_TABLE',
    'LETTERS_EMOJI',
    'LETTERS_TABLE',
    'EMOJIS_TABLE',
    'NUMBERS_EMOJI',
    'NUMBERS_TABLE',
    'Channels',
    'StaffRoles',
    'ExtraRoles'
)

FIRST_JANUARY_1970 = datetime(1970, 1, 1, 0, 0, 0, 0)
ALLOWED_CHARACTERS = tuple(st.printable)
EDGE_CHARACTERS_CASES = {
    '@': 'a',
    '0': 'o',
    '1': 'i',
    '$': 's',
    '!': 'i',
    '9': 'g',
    '5': 's',
}
EDGE_CHARACTERS_TABLE = str.maketrans(EDGE_CHARACTERS_CASES)
PUNCTUATIONS_AND_DIGITS = tuple(list(st.punctuation) + list(st.digits))
PAD_TABLE = str.maketrans({k: '' for k in PUNCTUATIONS_AND_DIGITS})

LETTERS_EMOJI = {
    'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩',
    'e': '🇪', 'f': '🇫', 'g': '🇬', 'h': '🇭',
    'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱',
    'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵',
    'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
    'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽',
    'y': '🇾', 'z': '🇿'
}
NUMBERS_EMOJI = {
    '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
    '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣',
    '8': '8️⃣', '9': '9️⃣'
}
LETTERS_TABLE = str.maketrans(LETTERS_EMOJI)
NUMBERS_TABLE = str.maketrans(NUMBERS_EMOJI)

EMOJIS_TABLE = str.maketrans({v: k for k, v in LETTERS_EMOJI.items()})


class Channels(NamedTuple):
    verify = 1121949315137544292

    rules = 1116784327359991918
    news = 1116785847203790929
    welcome = 1121924923158450237
    intros = 1121913011645460600
    how_to = 1122980121909919916

    general = 1116770347384045618
    venting = 1116853934972211351

    bots = 1116854686759268352
    memes = 1116854697823830047
    shitpost = 1116854708234096650

    selfies = 1122615397678583898
    photos = 1122615415240130691
    videos = 1122615471087292529
    fanart = 1116854071538761788
    random_art = 1116854139683614910

    staff_chat = 1116786173621309481
    bot_commands = 1117148228941525012
    ideas = 1117893777424666634
    lore_shit = 1117957572541026344

    logs = 1117162498735476767
    messages_logs = 1117162512438284338
    moderation_logs = 1121924279655743548
    github = 1117162553106239559
    discord_notifications = 1116784327359991919
    roblox_logs = 1117941905376956519


class StaffRoles(NamedTuple):
    owner = 1116783793605447700
    admin = 1122615777707700344
    mod = 1122615803225854022

    all = (owner, admin, mod)


class ExtraRoles(NamedTuple):
    unverified = 1121949200414949447
    booster = 1122887263001509979
    bot = 1122971950566875227
    muted = 1122972184600649728
