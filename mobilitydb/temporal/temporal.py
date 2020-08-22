from abc import abstractmethod
import warnings

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn("psycopg2 not installed", ImportWarning)


class Temporal:
    """
    Abstract class for representing temporal values of any duration.
    """

    @property
    def pymeos_deserializer_type(self):
        raise NotImplementedError()

    @property
    def pymeos_range_type(self):
        raise NotImplementedError()

    # Psycopg2 interface.
    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self

    def getquoted(self):
        return "'{}'".format(self.__str__())

    # End Psycopg2 interface.

    @classmethod
    def read_from_cursor(cls, value, cursor=None):
        if not value:
            return None
        return cls.pymeos_deserializer_type(value).nextTemporal()

    @classmethod
    def write(cls, value):
        return value.__str__()

    @property
    def valueRange(self):
        """
        Range of values taken by the temporal value as defined by its minimum and maximum value
        """
        return self.pymeos_range_type(self.minValue, self.maxValue, True, True)
