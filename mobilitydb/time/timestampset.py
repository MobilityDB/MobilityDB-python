from datetime import datetime, timedelta
from dateutil.parser import parse
from .period import Period
import warnings

from pymeos.time import TimestampSet as MEOSTimestampSet

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn('psycopg2 not installed', ImportWarning)


class TimestampSet(MEOSTimestampSet):
    """
    Class for representing lists of distinct timestamp values.

    ``TimestampSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TimestampSet('{2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01, 2019-09-11 00:00:00+01}')

    Another possibility is to give a tuple or list of composing timestamps,
    which can be instances of ``str`` or ``datetime``. The composing timestamps
    must be given in increasing order.

        >>> TimestampSet({'2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'})
        >>> TimestampSet({parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), parse('2019-09-11 00:00:00+01')})

    """

    # Psycopg2 interface.
    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self

    def getquoted(self):
        return "'{}'".format(self.__str__())
    # End Psycopg2 interface.

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TimestampSet(value)

    @staticmethod
    def write(value):
        if not isinstance(value, TimestampSet):
            raise ValueError('Value must be an instance of TimestampSet class')
        return value.__str__()

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.timestamps!r})')
