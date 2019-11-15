import re


class STBOX:
    __slots__ = ['xmin', 'ymin', 'zmin', 'tmin', 'xmax', 'ymax', 'zmax', 'tmax', 'flags']

    def __init__(self, value=None):
        self.flags = 0x00
        if isinstance(value, str) and value is not None:
            values = None
            if 'STBOX' in value:
                if 'ZT' in value:
                    self.flags = self.flags | 0x04
                    self.flags = self.flags | 0x08
                    self.flags = self.flags | 0x10
                elif 'Z' in value:
                    self.flags = self.flags | 0x04
                    self.flags = self.flags | 0x08
                elif 'T' in value:
                    self.flags = self.flags | 0x04
                    self.flags = self.flags | 0x10
                values = value.replace("STBOX", '').replace('ZT', '').replace('Z', '').replace('T', ''). \
                    replace('(', '').replace(')', '').split(',')
            elif 'GEODSTBOX' in value:
                if 'T' in value:
                    self.flags = self.flags | 0x04
                    self.flags = self.flags | 0x08
                    self.flags = self.flags | 0x10
                    self.flags = self.flags | 0x20
                else:
                    self.flags = self.flags | 0x04
                    self.flags = self.flags | 0x08
                    self.flags = self.flags | 0x20
                values = value.replace("GEODSTBOX", '').replace('T', ''). \
                    replace('(', '').replace(')', '').split(',')

            if self.flags & 0x04 and self.flags & 0x08 and self.flags & 0x10:
                self.xmin = float(values[0])
                self.xmax = float(values[4])
                self.ymin = float(values[1])
                self.ymax = float(values[5])
                self.zmin = float(values[2])
                self.zmax = float(values[6])
                self.tmin = format(values[3])
                self.tmax = format(values[7])
            elif self.flags & 0x04 and self.flags & 0x08 and not self.flags & 0x10:
                self.xmin = float(values[0])
                self.xmax = float(values[3])
                self.ymin = float(values[1])
                self.ymax = float(values[4])
                self.zmin = float(values[2])
                self.zmax = float(values[5])
            elif self.flags & 0x04 and not self.flags & 0x08 and self.flags & 0x10:
                self.xmin = float(values[0])
                self.xmax = float(values[3])
                self.ymin = float(values[1])
                self.ymax = float(values[4])
                self.tmin = format(values[2])
                self.tmax = format(values[5])
            else:
                self.xmin = float(values[0])
                self.xmax = float(values[2])
                self.ymin = float(values[1])
                self.ymax = float(values[3])

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
            elif self.flags & 0x04 and self.flags & 0x08 and not self.flags & 0x10:
                return "STBOX Z((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.zmin,
                                                                self.xmax, self.ymax, self.zmax)
            elif self.flags & 0x04 and not self.flags & 0x08 and self.flags & 0x10:
                return "STBOX T((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.tmin,
                                                                self.xmax, self.ymax, self.tmax)
            else:
                return "STBOX ((%s, %s), (%s, %s))" % (self.xmin, self.ymin, self.xmax, self.ymax)
