from dateutil.parser import parse
import re


class TBOX:
    __slots__ = ['xmin', 'tmin', 'xmax', 'tmax', 'flags']

    def __init__(self, *args):
        try:
            if len(args) == 1 and isinstance(args[0], str):
                self.parseFromString(args[0])
            elif len(args) == 2:
                try:
                    self.xmin = float(args[0])
                    self.xmax = float(args[1])
                    self.flags = 0x04
                except:
                    self.tmin = parse(args[0])
                    self.tmax = parse(args[1])
                    self.flags = 0x10
            elif len(args) == 4:
                self.xmin = float(args[0])
                self.tmin = parse(args[1])
                self.xmax = float(args[2])
                self.tmax = parse(args[3])
                self.flags = 0x04 | 0x10
        except:
            raise Exception("ERROR: Wrong parameters")

    def parseFromString(self, value):
        values = value.replace("TBOX", '').replace('(', '').replace(')', '').split(',')
        self.flags = 0x00
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
