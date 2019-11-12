from .period import PERIOD
import re


class PERIODSET:
    __slots__ = ['periodList']

    # constructor is missing
    def __init__(self, value=None):
        sequenceList = re.findall("((\[).+?\])+", value)
        print(sequenceList[0])

    def numPeriods(self):
        return len(self.periodList)

    def startPeriod(self):
        return self.periodList[0]

    def endPeriod(self):
        return self.periodList[self.numPeriods() - 1]

    def periods(self):
        return [period for period in self.periodList]
