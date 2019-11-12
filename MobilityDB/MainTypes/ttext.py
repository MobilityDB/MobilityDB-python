from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TTEXT(TEMPORAL):
    BaseValueClass = str

    def __init__(self, value=None):
        if isinstance(value, str):
            self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
        else:
            self.SubClass = value

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TTEXT(MobilityDBReader.readTemporalType(TTEXT, value))

    def __str__(self):
        if len(self.__class__.__bases__) == 2:
            return self.__class__.__bases__[0].__name__ + self.SubClass.__str__()
        else:
            return self.__class__.__name__ + self.SubClass.__str__()


class TTEXTINST(TTEXT, TEMPORALINST):

    def __init__(self, value=None):
        super().__init__(value)


class TTEXTI(TTEXT, TEMPORALI):

    def __init__(self, value=None):
        super().__init__(value)


class TTEXTSEQ(TTEXT, TEMPORALSEQ):

    def __init__(self, value=None):
        super().__init__(value)


class TTEXTS(TTEXT, TEMPORALS):

    def __init__(self, value=None):
        super().__init__(value)
