import datetime
from bdateutil.parser import parse


class PERIOD:
    __slots__ = ['lowerBound', 'upperBound', 'lowerBound_inc', 'upperBound_inc']

    # Missing arguments (lower_inc, upper_inc)
    def __init__(self, lower=None, upper=None):
        if isinstance(lower, str) and isinstance(upper, str):
            self.lowerBound = parse(lower)
            self.upperBound = parse(upper)
        elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
            self.lowerBound = lower
            self.upperBound = upper
        else:
            raise Exception("ERROR:  Could not parse period value")

    def lower(self):
        return self.lowerBound

    def upper(self):
        return self.upperBound

    def lower_inc(self):
        return self.lowerBound_inc

    def upper_inc(self):
        return self.upperBound_inc

    def __str__(self):
        return self.__class__.__name__+'({}, {})'.format(self.lowerBound, self.upperBound)
