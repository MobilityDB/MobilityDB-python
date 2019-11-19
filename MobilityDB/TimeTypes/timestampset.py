from .period import PERIOD
from bdateutil.parser import parse


class TIMESTAMPSET:
    __slots__ = ['_datetimeList']

    def __init__(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], str):
            ts = argv[0].strip()
            if ts[0] == '{' and ts[-1] == '}':
                ts = ts[1:]
                ts = ts[:-1]
                self._datetimeList = []
                times = ts.split(",")
                for time in times:
                    self._datetimeList.append(parse(time.strip()))
                if not self.__valid():
                    raise Exception("ERROR:  The timestamp values must be increasing")
            else:
                raise Exception("ERROR:  Could not parse timestamp set value")
        else:
            self._datetimeList = []
            for arg in argv:
                self._datetimeList.append(parse(arg))
            if not self.__valid():
                raise Exception("ERROR:  The timestamp values must be increasing")

    def __valid(self):
        return all(x < y for x, y in zip(self._datetimeList, self._datetimeList[1:]))

    def timespan(self):
        return PERIOD(self._datetimeList[0], self._datetimeList[-1], True, True)

    def numTimestamps(self):
        return len(self._datetimeList)

    def startTimestamp(self):
        return self._datetimeList[0]

    def endTimestamp(self):
        return self._datetimeList[-1]

    def timestampN(self, n):
        # 1-based
        if 0 < n <= len(self._datetimeList):
            return self._datetimeList[n - 1]
        else:
            raise Exception("ERROR: there is no value at this index")

    def timestamps(self):
        return self._datetimeList

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(other._datetimeList) == len(self._datetimeList) and \
                    set(other._datetimeList).intersection(self._datetimeList):
                return True
        return False

    def __str__(self):
        return "'{{{}}}'".format(', '.join('{}'.format(datetime.__str__())
                                           for datetime in self._datetimeList))
