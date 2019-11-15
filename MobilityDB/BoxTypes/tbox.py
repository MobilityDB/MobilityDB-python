import re


class TBOX:
    __slots__ = ['xmin', 'tmin', 'xmax', 'tmax']

    def __init__(self, value=None):
        if isinstance(value, str) and value is not None:
            values = value.replace("TBOX", '').replace('(', '').replace(')', '').split(',')
            if re.match(r'^-?\d+(?:\.\d+)?$', values[0].strip()) is not None:
                self.xmin = float(values[0])
                self.xmax = float(values[2])
            else:
                self.xmin = ''
                self.xmax = ''
            if len(values[1]) >= 4 and len(values[3]) >= 4:
                self.tmin = format(values[1])
                self.tmax = format(values[3])
            else:
                self.tmin = ''
                self.tmax = ''

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBOX(value)

    def __str__(self):
        return "TBOX((%s, %s), (%s, %s))" % (self.xmin, self.tmin, self.xmax, self.tmax)
