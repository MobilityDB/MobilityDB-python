import datetime
from bdateutil.parser import parse


class PERIOD:
    __slots__ = ['lowerT', 'upperT', 'lowerT_inc', 'upperT_inc']

    # Missing arguments (lower_inc, upper_inc)
    def __init__(self, lower=None, upper=None):
        if isinstance(lower, str) and isinstance(upper, str):
            self.lowerT = parse(lower)
            self.upperT = parse(upper)
        elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
            self.lowerT = lower
            self.upperT = upper
        else:
            raise Exception("ERROR:  Could not parse period value")

    def lower(self):
        return self.lowerT

    def upper(self):
        return self.upperT

    def __str__(self):
        return self.__class__.__name__+'({}, {})'.format(self.lowerT, self.upperT)
