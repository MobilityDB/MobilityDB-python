from .period import PERIOD
import re

class PERIODSET:
    __slots__ = ['periodList']

    def __init__(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], str):
            ps = argv[0].strip()
            if ps[0] == '{' and ps[-1] == '}':
                ps = ps[1:]
                ps = ps[:-1]
                self.periodList = []
                p = re.compile('[\[|\(].*?[^\]\)][\]|\)]')
                periods = p.findall(ps)
                for period in periods:
                    self.periodList.append(PERIOD(period))
            else:
                raise Exception("ERROR:  Could not parse period set value")
        else:
            self.periodList = []
            for arg in argv:
                self.periodList.append(PERIOD(arg))

    # constructor is missing
    #def __init__(self, value=None):
        #value = value.replace('{', '').replace('}', '')

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
            raise Exception("ERROR: out of range")

    def periods(self):
        return [period for period in self.periodList]

    def __str__(self):
        #return "{}{{{}}}".format("", self.periods())
        return "'{{{}}}'".format(', '.join('{}'.format(period.__str__().replace("'",""))
            for period in self.periodList))
