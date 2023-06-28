import datetime
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from .formats import plural, human_join, format_dt as format_dt
from disnake.ext import commands
import re

# Monkey patch mins and secs into the units
units = pdt.pdtLocales['en_US'].units
units['minutes'].append('mins')
units['seconds'].append('secs')

__all__ = (
    'ShortTime',
    'HumanTime',
    'Time',
    'FutureTime',
    'UserFriendlyTime',
    'human_timedelta',
    'format_relative',
)


class ShortTime:
    compiled = re.compile("""(?:(?P<years>[0-9])(?:years?|yrs|yr|y))?             # e.g. 2y
                             (?:(?P<months>[0-9]{1,2})(?:months?|month|mo))?     # e.g. 2months
                             (?:(?P<weeks>[0-9]{1,4})(?:weeks?|week|w))?        # e.g. 10w
                             (?:(?P<days>[0-9]{1,5})(?:days?|day|d))?          # e.g. 14d
                             (?:(?P<hours>[0-9]{1,5})(?:hours?|hour|hrs|hr|h))?        # e.g. 12h
                             (?:(?P<minutes>[0-9]{1,5})(?:minutes?|minute|mins|min|m))?    # e.g. 10m
                             (?:(?P<seconds>[0-9]{1,5})(?:seconds?|second|secs|sec|s))?    # e.g. 15s
                          """, re.VERBOSE | re.IGNORECASE)

    def __init__(self, argument, *, now=None):
        match = self.compiled.fullmatch(argument)
        if match is None or not match.group(0):
            raise commands.BadArgument('invalid time provided')

        data = {k: int(v) for k, v in match.groupdict(default=0).items()}
        now = now or datetime.datetime.now(datetime.timezone.utc)
        self.dt = now + relativedelta(**data)

    @classmethod
    async def convert(cls, ctx, argument):
        return cls(argument, now=ctx.message.created_at)


class HumanTime:
    calendar = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)

    def __init__(self, argument, *, now=None):
        now = now or datetime.datetime.utcnow()
        dt, status = self.calendar.parseDT(argument, sourceTime=now)
        if not status.hasDateOrTime:
            raise commands.BadArgument('invalid time provided, try e.g. "tomorrow" or "3 days"')

        if not status.hasTime:
            # replace it with the current time
            dt = dt.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)

        self.dt = dt
        self._past = dt < now

    @classmethod
    async def convert(cls, ctx, argument):
        return cls(argument, now=ctx.message.created_at)


class Time(HumanTime):
    def __init__(self, argument, *, now=None):
        try:
            o = ShortTime(argument, now=now)
        except Exception:
            super().__init__(argument)
        else:
            self.dt = o.dt
            self._past = False


class FutureTime(Time):
    def __init__(self, argument, *, now=None):
        super().__init__(argument, now=now)

        if self._past:
            raise commands.BadArgument('this time is in the past')


class UserFriendlyTime:
    """That way quotes aren't absolutely necessary."""

    async def check_constraints(self, now, remaining):
        if self.dt < now:
            raise commands.BadArgument('This time is in the past.')

        if not remaining:
            remaining = None

        self.arg = remaining
        return self

    def copy(self):
        cls = self.__class__
        obj = cls.__new__(cls)
        return obj

    async def convert(self, argument):
        # Create a copy of ourselves to prevent race conditions from two
        # events modifying the same instance of a converter
        result = self.copy()
        calendar = HumanTime.calendar
        regex = ShortTime.compiled
        now = datetime.datetime.utcnow()

        match = regex.match(argument)
        if match is not None and match.group(0):
            data = {k: int(v) for k, v in match.groupdict(default=0).items()}
            remaining = argument[match.end():].strip()
            result.dt = now + relativedelta(**data)
            return await result.check_constraints(now, remaining)

        # apparently nlp does not like "from now"
        # it likes "from x" in other cases though so let me handle the 'now' case
        if argument.endswith('from now'):
            argument = argument[:-8].strip()

        if argument[0:2] == 'me':
            # starts with "me to", "me in", or "me at "
            if argument[0:6] in ('me to ', 'me in ', 'me at '):
                argument = argument[6:]

        elements = calendar.nlp(argument, sourceTime=now)
        if elements is None or len(elements) == 0:
            raise commands.BadArgument('Invalid time provided, try e.g. "tomorrow" or "3 days".')

        # handle the following cases:
        # "date time" foo
        # date time foo
        # foo date time

        # first the first two cases:
        dt, status, begin, end, dt_string = elements[0]

        if not status.hasDateOrTime:
            raise commands.BadArgument('Invalid time provided, try e.g. "tomorrow" or "3 days".')

        if begin not in (0, 1) and end != len(argument):
            raise commands.BadArgument('Time is either in an inappropriate location, which '
                                       'must be either at the end or beginning of your input, '
                                       'or I just flat out did not understand what you meant. Sorry.')

        if not status.hasTime:
            # replace it with the current time
            dt = dt.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)

        # if midnight is provided, just default to next day
        if status.accuracy == pdt.pdtContext.ACU_HALFDAY:
            dt = dt.replace(day=now.day + 1)

        if begin in (0, 1):
            if begin == 1:
                # check if it's quoted:
                if argument[0] != '"':
                    raise commands.BadArgument('Expected quote before time input...')

                if not (end < len(argument) and argument[end] == '"'):
                    raise commands.BadArgument('If the time is quoted, you must unquote it.')

                remaining = argument[end + 1:].lstrip(' ,.!')
            else:
                remaining = argument[end:].lstrip(' ,.!')
        elif len(argument) == end:
            remaining = argument[:begin].strip()

        return await result.check_constraints(now, remaining)


def human_timedelta(dt, *, source=None, accuracy=3, brief=False, suffix=True):
    now = source or datetime.datetime.now(datetime.timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)

    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)

    # Microsecond free zone
    now = now.replace(microsecond=0)
    dt = dt.replace(microsecond=0)

    # This implementation uses relativedelta instead of the much more obvious
    # divmod approach with seconds because the seconds approach is not entirely
    # accurate once you go over 1 week in terms of accuracy since you have to
    # hardcode a month as 30 or 31 days.
    # A query like "11 months" can be interpreted as "!1 months and 6 days"
    if dt > now:
        delta = relativedelta(dt, now)
        suffix = ''
    else:
        delta = relativedelta(now, dt)
        suffix = ' ago' if suffix else ''

    attrs = [
        ('year', 'y'),
        ('month', 'mo'),
        ('day', 'd'),
        ('hour', 'h'),
        ('minute', 'm'),
        ('second', 's'),
    ]

    output = []
    for attr, brief_attr in attrs:
        elem = getattr(delta, attr + 's')
        if not elem:
            continue

        if attr == 'day':
            weeks = delta.weeks
            if weeks:
                elem -= weeks * 7
                if not brief:
                    output.append(format(plural(weeks), 'week'))
                else:
                    output.append(f'{weeks}w')

        if elem <= 0:
            continue

        if brief:
            output.append(f'{elem}{brief_attr}')
        else:
            output.append(format(plural(elem), attr))

    if accuracy is not None:
        output = output[:accuracy]

    if len(output) == 0:
        return 'now'
    else:
        if not brief:
            return human_join(output, final='and') + suffix
        else:
            return ' '.join(output) + suffix


def format_relative(dt):
    return format_dt(dt, 'R')