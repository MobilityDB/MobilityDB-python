import datetime
import warnings
from dateutil.parser import parse

from pymeos.time import Period as MEOSPeriod

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn("psycopg2 not installed", ImportWarning)


class Period(MEOSPeriod):
    """
    Class for representing sets of contiguous timestamps between a lower and
    an upper bound. The bounds may be inclusive or not.

    ``Period`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> Period('(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)')

    Another possibility is to give a tuple of arguments as follows:

    * ``lower`` and ``upper`` are instances of ``str`` or ``datetime``
      specifying the bounds,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default, ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> Period('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01')
        >>> Period('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', False, True)
        >>> Period(parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'))
        >>> Period(parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), False, True)

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
        return Period(value)

    @staticmethod
    def write(value):
        if not isinstance(value, Period):
            raise ValueError("Value must be an instance of Period class")
        return value.__str__()

    def __repr__(self):
        return (
            f"{self.__class__.__name__ }"
            f"({self.lower!r}, {self.upper!r}, {self.lower_inc!r}, {self.upper_inc!r})"
        )
