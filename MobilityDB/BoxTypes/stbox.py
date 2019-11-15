import re


class STBOX:
    __slots__ = ['xmin', 'ymin', 'zmin', 'tmin', 'xmax', 'ymax', 'zmax', 'tmax', 'flags']

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            self.parseFromString(args[0])
        else:
            if len(args) >= 4:
                self.xmin = args[0]
                self.xmax = args[int(len(args) / 2)]
                self.ymin = args[1]
                self.ymax = args[1 + int(len(args) / 2)]
                self.flags = 0x04
            if len(args) >= 6:
                self.zmin = args[2]
                self.zmax = args[2 + int(len(args) / 2)]
                self.flags = self.flags | 0x08
            if len(args) == 8:
                self.tmin = args[int(len(args) / 2) - 1]
                self.tmax = args[(int(len(args) / 2) - 1) + int(len(args) / 2)]
                self.flags = self.flags | 0x10

    def parseFromString(self, value):
        if isinstance(value, str) and value is not None:
            values = None
            self.flags = 0x00
            if 'GEODSTBOX' in value:
                value = value.replace("GEODSTBOX", '')
                self.flags = self.flags | 0x04
                self.flags = self.flags | 0x08
                self.flags = self.flags | 0x20
                if 'T' in value:
                    self.flags = self.flags | 0x10
                values = value.replace('T', '').replace('(', '').replace(')', '').split(',')
            elif 'STBOX' in value:
                value = value.replace("STBOX", '')
                self.flags = self.flags | 0x04
                if 'ZT' in value:
                    self.flags = self.flags | 0x08
                    self.flags = self.flags | 0x10
                elif 'Z' in value:
                    self.flags = self.flags | 0x08
                elif 'T' in value:
                    self.flags = self.flags | 0x10
                values = value.replace('ZT', '').replace('Z', '').replace('T', ''). \
                    replace('(', '').replace(')', '').split(',')
            else:
                raise Exception("ERROR: Input must be STBOX")

            if self.flags & 0x04:
                self.xmin = float(values[0])
                self.xmax = float(values[int(len(values) / 2)])
                self.ymin = float(values[1])
                self.ymax = float(values[1 + int(len(values) / 2)])
            if self.flags & 0x08:
                self.zmin = float(values[2])
                self.zmax = float(values[2 + int(len(values) / 2)])
            if self.flags & 0x10:
                self.tmin = format(values[int(len(values) / 2) - 1])
                self.tmax = format(values[(int(len(values) / 2) - 1) + int(len(values) / 2)])

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return STBOX(value)

    def __str__(self):
        if self.flags & 0x20:
            if self.flags & 0x10:
                return "GEODSTBOX T((%s, %s, %s, %s), (%s, %s, %s, %s))" % (self.xmin, self.ymin, self.zmin, self.tmin,
                                                                            self.xmax, self.ymax, self.zmax, self.tmax)
            else:
                return "GEODSTBOX((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.zmin,
                                                                  self.xmax, self.ymax, self.zmax)
        else:
            if self.flags & 0x04 and self.flags & 0x08 and self.flags & 0x10:
                return "STBOX ZT((%s, %s, %s, %s), (%s, %s, %s, %s))" % (self.xmin, self.ymin, self.zmin, self.tmin,
                                                                         self.xmax, self.ymax, self.zmax, self.tmax)
            elif self.flags & 0x04 and self.flags & 0x08 and not (self.flags & 0x10):
                return "STBOX Z((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.zmin,
                                                                self.xmax, self.ymax, self.zmax)
            elif self.flags & 0x04 and not (self.flags & 0x08) and self.flags & 0x10:
                return "STBOX T((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.tmin,
                                                                self.xmax, self.ymax, self.tmax)
            else:
                return "STBOX ((%s, %s), (%s, %s))" % (self.xmin, self.ymin, self.xmax, self.ymax)
