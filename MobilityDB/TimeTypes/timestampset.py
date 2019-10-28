from bdateutil.parser import parse


class TIMESTAMPSET:
    __slots__ = ['timeList']

    def __init__(self, *argv):
        self.timeList = []
        for arg in argv:
            self.timeList.append(parse(arg))

    def __str__(self):
        return "{}'{{{}}}'".format(self.__class__.__name__, ', '.join('{}'.format(time.__str__())
                                                                      for time in self.timeList))
