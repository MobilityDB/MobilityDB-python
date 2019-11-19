import datetime
from bdateutil.parser import parse


class PERIOD:
    __slots__ = ['lowerBound', 'upperBound', 'lowerBound_inc', 'upperBound_inc']

    # Missing arguments (lower_inc, upper_inc)
    def __init__(self, lower, upper=None, lower_inc=None, upper_inc=None):
        if upper is None and isinstance(lower, str):
            lower = lower.strip()
            self.lowerBound_inc = True if lower[0] == '[' else False
            self.upperBound_inc = True if lower[len(lower) - 1] == ']' else False
            bounds = lower.split(',')
            bounds[0] = (bounds[0])[1:]
            bounds[1] = (bounds[1])[:-1]
            self.lowerBound = parse(bounds[0])
            self.upperBound = parse(bounds[1])
        elif isinstance(lower, str) and isinstance(upper, str):
            self.lowerBound = parse(lower)
            self.upperBound = parse(upper)
            self.lowerBound_inc = lower_inc if lower_inc is not None else True
            self.upperBound_inc = upper_inc if upper_inc is not None else False
        elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
            self.lowerBound = lower
            self.upperBound = upper
            self.lowerBound_inc = lower_inc if lower_inc is not None else True
            self.upperBound_inc = upper_inc if upper_inc is not None else False
        else:
            raise Exception("ERROR: Could not parse period value")
        if not self.__valid():
            raise Exception("ERROR: Invalid period arguments")

    def __valid(self):
        if self.lowerBound > self.upperBound:
            return False
        if self.lowerBound == self.upperBound and \
                (self.lowerBound_inc == False or self.upperBound_inc == False):
            return False
        return True

    def lower(self):
        return self.lowerBound

    def upper(self):
        return self.upperBound

    def lower_inc(self):
        return self.lowerBound_inc

    def upper_inc(self):
        return self.upperBound_inc

    def duration(self):
        return self

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.lowerBound != other.lowerBound or self.upperBound != other.upperBound or \
                    self.lowerBound_inc != other.lowerBound_inc or self.upperBound_inc != other.upperBound_inc:
                return False
        return True

    def __str__(self):
        lower_str = '[' if self.lowerBound_inc else '('
        upper_str = ']' if self.upperBound_inc else ')'
        return "'" + lower_str + '{}, {}'.format(self.lowerBound, self.upperBound) + upper_str + "'"
