import datetime

import pytz as pytz

_UTC = pytz.utc


def now():
    """
    Returns an aware or naive datetime.datetime in UTC.
    """
    return datetime.datetime.utcnow().replace(tzinfo=_UTC)
