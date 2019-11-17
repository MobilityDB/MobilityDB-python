from .temporal import TEMPORAL


class TEMPORALINST(TEMPORAL):
    __slots__ = ['value', 'time']
    Duration = 1

    def __init__(self, value=None, time=None):
        self.value = value
        self.time = time

    def __str__(self):
        if self.SubClass.__class__ == TEMPORALINST:
            return self.__class__.__bases__[0].__name__+" '"+self.SubClass.__str__()+"'"
        else:
            return "{}{}".format(self.value.__str__() + "@", self.time.__str__())
