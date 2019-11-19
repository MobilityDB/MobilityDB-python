from .period import PERIOD
import re

class PERIODSET:
    __slots__ = ['periodList']

    def __init__(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], str):
            ps = argv[0].strip()
            if ps[0] == '{' and ps[-1] == '}':
                self.periodList = []
                p = re.compile('[\[|\(].*?[^\]\)][\]|\)]')
                periods = p.findall(ps)
                for period in periods:
                    self.periodList.append(PERIOD(period))
            else:
                raise Exception("ERROR: Could not parse period set value")
        else:
            self.periodList = []
            for arg in argv:
                self.periodList.append(PERIOD(arg))

    @property
    def timespan(self):
        return PERIOD(self.periodList[0].lowerBound, self.periodList[-1].upperBound,
                      self.periodList[0].lowerBound_inc, self.periodList[-1].upperBound_inc)

    def numTimestamps(self):
        return len(self.timestamps())

    @property
    def startTimestamp(self):
        return self.periodList[0].lowerBound

    @property
    def endTimestamp(self):
        return self.periodList[-1].upperBound

    @property
    def timestampN(self, n):
        # 1-based
        if 0 < n <= len(self.timestamps()):
            return (self.timestamps())[n - 1]
        else:
            raise Exception("ERROR: there is no value at this index")

    @property
    def timestamps(self):
        timestamps = []
        for period in self.periodList:
            timestamps.append(period.lowerBound)
            timestamps.append(period.upperBound)
        # Remove duplicates
        timestamps = list(dict.fromkeys(timestamps))
        return timestamps

    def numPeriods(self):
        return len(self.periodList)

    def startPeriod(self):
        return self.periodList[0]

    def endPeriod(self):
        return self.periodList[self.numPeriods() - 1]

    def periodN(self, n):
        if 0 <= n < len(self.periodList):
            return self.periodList[n]
        else:
            raise Exception("ERROR: Out of range")

    def periods(self):
        return [period for period in self.periodList]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(other.periodList) == len(self.periodList) and set(other.periodList).intersection(self.periodList):
                return True
        return False

    def __str__(self):
        return "'{{{}}}'".format(', '.join('{}'.format(period.__str__().replace("'",""))
            for period in self.periodList))
