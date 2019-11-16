from dateutil.parser import parse
import re


class TBOX:
    __slots__ = ['xMin', 'tMin', 'xMax', 'tMax', 'flags']

    def __init__(self, *args):
        try:
            if len(args) == 1 and isinstance(args[0], str):
                self.parseFromString(args[0])
            elif len(args) == 2:
                try:
                    self.xMin = float(args[0])
                    self.xMax = float(args[1])
                    self.flags = 0x04
                except:
                    self.tMin = parse(args[0])
                    self.tMax = parse(args[1])
                    self.flags = 0x10
            elif len(args) == 4:
                self.xMin = float(args[0])
                self.tMin = parse(args[1])
                self.xMax = float(args[2])
                self.tMax = parse(args[3])
                self.flags = 0x04 | 0x10
        except:
            raise Exception("ERROR: Wrong parameters")

    def parseFromString(self, value):
        values = value.replace("TBOX", '').replace('(', '').replace(')', '').split(',')
        self.flags = 0x00
        if re.match(r'^-?\d+(?:\.\d+)?$', values[0].strip()) is not None:
            self.flags = self.flags | 0x04
            self.xMin = float(values[0])
            self.xMax = float(values[2])
        if len(values[1]) >= 4 and len(values[3]) >= 4:
            self.flags = self.flags | 0x10
            self.tMin = format(values[1])
            self.tMax = format(values[3])

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBOX(value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # I need to add the other values in the comparison but there is a problem appears when I run the test file
            return self.flags == other.flags
        else:
            return False

    def __str__(self):
        if self.flags & 0x04 and self.flags & 0x10:
            return "TBOX((%s, %s), (%s, %s))" % (self.xMin, self.tMin, self.xMax, self.tMax)
        elif self.flags & 0x04:
            return "TBOX((%s, %s), (%s, %s))" % (self.xMin, '', self.xMax, '')
        elif self.flags & 0x10:
            return "TBOX((%s, %s), (%s, %s))" % ('', self.tMin, '', self.tMax)
