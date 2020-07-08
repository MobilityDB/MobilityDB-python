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

    BaseClass = None
    """
    Class of the base type, for example, ``float`` for ``TFloat``
    """

    BaseClassDiscrete = None
    """
    Boolean value that states whether the base type is discrete or not, 
    for example, ``True`` for ``int`` and ``False`` for ``float``
    """

    ComponentClass = None
    """
    Class of the components, for example, 

    1. ``TFloatInst`` for both ``TFloatI`` and ``TFloatSeq``
    2. ``TFloatSeq`` for ``TFloatS``.
    """

    @classmethod
    @abstractmethod
    def duration(cls):
        """
        Duration of the temporal value, that is, one of ``'Instant'``,
        ``'InstantSet'``, ``'Sequence'``, or ``'SequenceSet'``.
        """
        pass

    @property
    @abstractmethod
    def getValues(self):
        """
        List of distinct values taken by the temporal value.
        """
        pass

    @property
    @abstractmethod
    def startValue(self):
        """
        Start value.
        """
        pass

    @property
    @abstractmethod
    def endValue(self):
        """
        End value.
        """
        pass

    @property
    @abstractmethod
    def minValue(self):
        """
        Minimum value.
        """
        pass

    @property
    @abstractmethod
    def maxValue(self):
        """
        Maximum value.
        """
        pass

    @property
    @abstractmethod
    def getTime(self):
        """
        Period set on which the temporal value is defined.
        """
        pass

    @property
    @abstractmethod
    def timespan(self):
        """
        Interval on which the temporal value is defined.
        """
        pass

    @property
    @abstractmethod
    def period(self):
        """
        Period on which the temporal value is defined ignoring potential time gaps.
        """
        pass

    @property
    @abstractmethod
    def numInstants(self):
        """
        Number of distinct instants.
        """
        pass

    @property
    @abstractmethod
    def startInstant(self):
        """
         Start instant.
        """
        pass

    @property
    @abstractmethod
    def endInstant(self):
        """
        End instant.
        """
        pass

    @abstractmethod
    def instantN(self, n):
        """
        N-th instant.
        """
        pass

    @property
    @abstractmethod
    def instants(self):
        """
        List of instants.
        """
        pass

    @property
    @abstractmethod
    def numTimestamps(self):
        """
        Number of distinct timestamps.
        """
        pass

    @property
    @abstractmethod
    def startTimestamp(self):
        """
        Start timestamp.
        """
        pass

    @property
    @abstractmethod
    def endTimestamp(self):
        """
        End timestamp.
        """
        pass

    @abstractmethod
    def timestampN(self, n):
        """
        N-th timestamp.
        """
        pass

    @property
    @abstractmethod
    def timestamps(self):
        """
        List of timestamps.
        """
        pass

    @abstractmethod
    def shift(self, timedelta):
        """
        Shift the temporal value by a time interval
        """
        pass

    @abstractmethod
    def intersectsTimestamp(self, datetime):
        """
        Does the temporal value intersect the timestamp?
        """
        pass

    @abstractmethod
    def intersectsTimestampSet(self, timestampset):
        """
        Does the temporal value intersect the timestamp set?
        """
        pass

    @abstractmethod
    def intersectsPeriod(self, period):
        """
        Does the temporal value intersect the period?
        """
        pass

    @abstractmethod
    def intersectsPeriodSet(self, periodset):
        """
        Does the temporal value intersect the period set?
        """
        pass

    # Psycopg2 interface.
    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self

    def getquoted(self):
        return "'{}'".format(self.__str__())
    # End Psycopg2 interface.

    # Comparisons are missing
    def __eq__(self, other):
        """
        Equality
        """
        pass

    def __str__(self):
        """
        String
        """
        pass

    def __repr__(self):
        """
        Representation
        """
        pass
