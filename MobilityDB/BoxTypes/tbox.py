from MobilityDB.TemporalTypes import *

from MobilityDB.MobilityDBReader import MobilityDBReader


class TBOX:
    __slots__ = ['x1', 't1', 'x2', 't2']

    def __init__(self, minPart=None, maxPart=None):
        if isinstance(minPart, str) and maxPart is None:
            values = minPart.replace("TBOX", '').replace('(', '').replace(')', '').split(',')
            self.x1 = float(values[0])
            self.x2 = float(values[2])
            self.t1 = format(values[1])
            self.t2 = format(values[3])
        else:
            self.x1 = float(minPart[0])
            self.x2 = float(maxPart[0])
            self.t1 = format(minPart[1])
            self.t2 = format(maxPart[1])

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBOX(value)

    def __str__(self):
        return "TBOX(("+str(self.x1)+','+self.t1+"),("+str(self.x2)+','+self.t2+"))"

