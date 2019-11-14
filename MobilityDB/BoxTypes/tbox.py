import re


class TBOX:
    __slots__ = ['x1', 't1', 'x2', 't2']

    def __init__(self, value=None):
        if isinstance(value, str) and value is not None:
            values = value.replace("TBOX", '').replace('(', '').replace(')', '').split(',')
            if re.match(r'^-?\d+(?:\.\d+)?$', values[0]) is not None:
                self.x1 = float(values[0])
                self.x2 = float(values[2])
            else:
                self.x1 = None
                self.x2 = None
            if len(values[1]) >= 4 and len(values[3]) >= 4:
                self.t1 = format(values[1])
                self.t2 = format(values[3])
            else:
                self.t1 = None
                self.t2 = None

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBOX(value)

    def __str__(self):
        if self.x1 is None and self.x2 is None:
            return "TBOX((%s,%s), (%s,%s))" % ('', self.t1, '', self.t2)
        elif self.t1 is None and self.t2 is None:
            return "TBOX((%s, %s), (%s, %s))" % (self.x1, '', self.x2, '')
        else:
            return "TBOX((%s, %s), (%s, %s))" % (self.x1, self.t1, self.x2, self.t2)
