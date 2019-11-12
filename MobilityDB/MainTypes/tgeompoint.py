from postgis import Point
from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TGEOMPOINT(TEMPORAL):
    BaseValueClass = Point

    def __init__(self, value=None):
        if isinstance(value, str):
            self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
        else:
            self.SubClass = value

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TGEOMPOINT(MobilityDBReader.readTemporalType(TGEOMPOINT, value))

    def __str__(self):
        if len(self.__class__.__bases__) == 2:
            return self.__class__.__bases__[0].__name__ + self.SubClass.__str__()
        else:
            return self.__class__.__name__ + self.SubClass.__str__()


class TGEOMPOINTINST(TGEOMPOINT, TEMPORALINST):

    def __init__(self, value=None):
        super().__init__(value)


class TGEOMPOINTI(TGEOMPOINT, TEMPORALI):

    def __init__(self, value=None):
        super().__init__(value)


class TGEOMPOINTSEQ(TGEOMPOINT, TEMPORALSEQ):

    def __init__(self, value=None):
        super().__init__(value)


class TGEOMPOINTS(TGEOMPOINT, TEMPORALS):

    def __init__(self, value=None):
        super().__init__(value)
