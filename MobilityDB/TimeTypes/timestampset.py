from .period import PERIOD

class TIMESTAMPSET:
    __slots__ = ['timeList']

    def __init__(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], str):
            ts = argv[0].strip()
            if ts[0] == '{' and ts[-1] == '}':
                ts = ts[1:]
                ts = ts[:-1]
                self.timeList = []
                times = ts.split(",")
                for time in times:
                    self.timeList.append(format(time.strip()))
            else:
                raise Exception("ERROR:  Could not parse timestamp set value")
        else:
            self.timeList = []
            for arg in argv:
                self.timeList.append(format(arg))

    def timespan(self):
        return PERIOD(min(time for time in self.timeList),
                      max(time for time in self.timeList), True, True)

    def numTimestamps(self):
        return len(self.timeList)

    def startTimestamp(self):
        return self.timeList[0]

    def endTimestamp(self):
        return self.timeList[-1]

    def timestampN(self, n):
        # 1-based
        if 0 < n <= len(self.timeList):
            return self.timeList[n - 1]
        else:
            raise Exception("ERROR: there is no value at this index")

    def timestamps(self):
        return self.timeList

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(other.timeList) == len(self.timeList) and set(other.timeList).intersection(self.timeList):
                return True
        return False

    def __str__(self):
        return "'{{{}}}'".format(', '.join('{}'.format(time.__str__())
            for time in self.timeList))
