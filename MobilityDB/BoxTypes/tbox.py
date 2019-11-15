import re


class TBOX:
    __slots__ = ['xmin', 'tmin', 'xmax', 'tmax', 'flags']

    def __init__(self, value=None):
        self.flags = 0x00
        if isinstance(value, str) and value is not None:
            values = value.replace("TBOX", '').replace('(', '').replace(')', '').split(',')
            if re.match(r'^-?\d+(?:\.\d+)?$', values[0].strip()) is not None:
                self.flags = self.flags | 0x04
                self.xmin = float(values[0])
                self.xmax = float(values[2])
            if len(values[1]) >= 4 and len(values[3]) >= 4:
                self.flags = self.flags | 0x10
                self.tmin = format(values[1])
                self.tmax = format(values[3])

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBOX(value)

    def __str__(self):
        if self.flags & 0x04 and self.flags & 0x10:
            return "TBOX((%s, %s), (%s, %s))" % (self.xmin, self.tmin, self.xmax, self.tmax)
        elif self.flags & 0x04:
            return "TBOX((%s, %s), (%s, %s))" % (self.xmin, '', self.xmax, '')
        elif self.flags & 0x10:
            return "TBOX((%s, %s), (%s, %s))" % ('', self.tmin, '', self.tmax)
