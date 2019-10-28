import datetime
from bdateutil.parser import parse


class PERIOD:
    __slots__ = ['lower', 'upper']

    def __init__(self, lower=None, upper=None):
        if isinstance(lower, str) and isinstance(upper, str):
            self.lower = parse(lower)
            self.upper = parse(upper)
        elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
            self.lower = lower
            self.upper = upper
        else:
            raise Exception("ERROR:  Could not parse period value")

    def __str__(self):
        return self.__class__.__name__+'({}, {})'.format(self.lower, self.upper)
