import re
from .period import Period
import warnings

from pymeos.time import Period as MEOSPeriod, PeriodSet as MEOSPeriodSet

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn('psycopg2 not installed', ImportWarning)


class PeriodSet(MEOSPeriodSet):
    """
    Class for representing lists of disjoint periods.

    ``PeriodSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> PeriodSet('{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01], [2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]}')

    Another possibility is to give a set specifying the composing
    periods, which can be instances  of ``str`` or ``Period``.

        >>> PeriodSet({'[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]', '[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]'})
        >>> PeriodSet({Period('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]'), Period('[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]')})

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
        return PeriodSet(value)

    @staticmethod
    def write(value):
        if not isinstance(value, PeriodSet):
            raise ValueError('Value must be an instance of PeriodSet class')
        return value.__str__()

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.periods!r})')
