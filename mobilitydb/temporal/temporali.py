from datetime import timedelta
from mobilitydb.time import Period, PeriodSet
from mobilitydb.temporal import TemporalInstants
from mobilitydb.temporal.temporal_parser import parse_temporali


class TemporalI(TemporalInstants):
    """
    Abstract class for representing temporal values of instant set duration.
    """

    def __init__(self, *argv):
        self._instantList = []
        # Constructor with a single argument of type string
        if len(argv) == 1 and isinstance(argv[0], str):
            elements = parse_temporali(argv[0], 0)
            for inst in elements[2]:
                self._instantList.append(TemporalI.ComponentClass(inst[0], inst[1]))
        # Constructor with a single argument of type list
        elif len(argv) == 1 and isinstance(argv[0], list):
            # List of strings representing instant values
            if all(isinstance(arg, str) for arg in argv[0]):
                for arg in argv[0]:
                    self._instantList.append(TemporalI.ComponentClass(arg))
            # List of instant values
            elif all(isinstance(arg, TemporalI.ComponentClass) for arg in argv[0]):
                for arg in argv[0]:
                    self._instantList.append(arg)
            else:
                raise Exception("ERROR: Could not parse temporal instant set value")
        # Constructor with multiple arguments
        else:
            # Arguments are of type string
            if all(isinstance(arg, str) for arg in argv):
                for arg in argv:
                    self._instantList.append(TemporalI.ComponentClass(arg))
            # Arguments are of type instant
            elif all(isinstance(arg, TemporalI.ComponentClass) for arg in argv):
                for arg in argv:
                    self._instantList.append(arg)
            else:
                raise Exception("ERROR: Could not parse temporal instant set value")
        # Verify validity of the resulting instance
        self._valid()

    def _valid(self):
        if any(x._time > y._time for x, y in zip(self._instantList, self._instantList[1:])):
            raise Exception("ERROR: The timestamps of a temporal instant must be increasing")

    @classmethod
    def duration(cls):
        """
        Duration of the temporal value, that is, ``'InstantSet'``.
        """
        return "InstantSet"

    @property
    def getTime(self):
        """
        Period set on which the temporal value is defined.
        """
        return PeriodSet([inst.period for inst in self._instantList])

    @property
    def timespan(self):
        """
        Interval on which the temporal value is defined. It is zero for
        temporal values of instant set duration.
        """
        return timedelta(0)

    @property
    def period(self):
        """
        Period on which the temporal value is defined ignoring the potential time gaps.
        """
        return Period(self.startTimestamp, self.endTimestamp, True, True)

    def intersectsTimestamp(self, timestamp):
        """
        Does the temporal value intersect the timestamp?
        """
        return any(inst._time == timestamp for inst in self._instantList)

    def intersectsTimestampset(self, timestampset):
        """
        Does the temporal value intersect the timestamp set?
        """
        return any(inst._time == timestamp for inst in self._instantList for timestamp in timestampset._datetimeList)

    def intersectsPeriod(self, period):
        """
        Does the temporal value intersect the period?
        """
        return any(period.contains_timestamp(inst._time) for inst in self._instantList)

    def intersectsPeriodset(self, periodset):
        """
        Does the temporal value intersect the period set?
        """
        return any(period.contains_timestamp(inst._time) for inst in self._instantList for period in periodset._periodList)

    # Comparisons are missing
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._instantList == other._instantList:
                return True
        return False

    def __str__(self):
        return (f"'{{{TemporalInstants.__str__(self)}}}'")

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self._instantList!r})')