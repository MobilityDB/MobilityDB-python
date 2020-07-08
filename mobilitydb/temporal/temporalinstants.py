from .temporal import Temporal


class TemporalInstants(Temporal):
    """
    Abstract class for representing temporal values of instant set or
    sequence duration.
    """
    __slots__ = ['_instantList']

    @property
    def getValues(self):
        """
        List of distinct values taken by the temporal value.
        """
        return list(dict.fromkeys([inst.getValue for inst in self._instantList]))

    @property
    def startValue(self):
        """
        Start value.
        """
        return self._instantList[0].getValue

    @property
    def endValue(self):
        """
        End value.
        """
        return self._instantList[-1].getValue

    @property
    def minValue(self):
        """
        Minimum value.
        """
        return min(inst.getValue for inst in self._instantList)

    @property
    def maxValue(self):
        """
        Maximum value.
        """
        return max(inst.getValue for inst in self._instantList)

    @property
    def numInstants(self):
        """
        Number of instants.
        """
        return len(self._instantList)

    @property
    def startInstant(self):
        """
        Start instant.
        """
        return self._instantList[0]

    @property
    def endInstant(self):
        """
        End instant.
        """
        return self._instantList[-1]

    def instantN(self, n):
        """
        N-th instant.
        """
        # 1-based
        if 1 <= n <= len(self._instantList):
            return self._instantList[n - 1]
        else:
            raise Exception("ERROR: Out of range")

    @property
    def instants(self):
        """
        List of instants.
        """
        return self._instantList

    @property
    def numTimestamps(self):
        """
        Number of timestamps.
        """
        return len(self._instantList)

    @property
    def startTimestamp(self):
        """
        Start timestamp.
        """
        return self._instantList[0].getTimestamp

    @property
    def endTimestamp(self):
        """
        End timestamp.
        """
        return self._instantList[-1].getTimestamp

    def timestampN(self, n):
        """
        N-th timestamp.
        """
        # 1-based
        if 1 <= n <= len(self._instantList):
            return self._instantList[n - 1].getTimestamp
        else:
            raise Exception("ERROR: Out of range")

    @property
    def timestamps(self):
        """
        List of timestamps.
        """
        return [instant.getTimestamp for instant in self._instantList]

    def shift(self, timedelta):
        """
        Shift the temporal value by a time interval.
        """
        for inst in self._instantList:
            inst.getTimestamp += timedelta
        return self

    def __str__(self):
        return "{}".format(', '.join('{}'.format(instant.__str__().replace("'", ""))
            for instant in self._instantList))
