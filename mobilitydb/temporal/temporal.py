from abc import abstractmethod
import warnings

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn('psycopg2 not installed', ImportWarning)


class Temporal:
    """
    Abstract class for representing temporal values of any duration.
    """

    # Psycopg2 interface.
    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self

    def getquoted(self):
        return "'{}'".format(self.__str__())
    # End Psycopg2 interface.
