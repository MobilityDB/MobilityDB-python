class TIMESTAMPSET:
    __slots__ = ['timeList']

    def __init__(self, *argv):
        self.timeList = []
        for arg in argv:
            self.timeList.append(format(arg))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(other.timeList) == len(self.timeList) and set(other.timeList).intersection(self.timeList):
                return True
        return False

    def __str__(self):
        return "'{{{}}}'".format(', '.join('{}'.format(time.__str__())
            for time in self.timeList))
