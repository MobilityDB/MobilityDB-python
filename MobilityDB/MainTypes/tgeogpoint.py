from postgis import Point
from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TGEOGPOINT(TEMPORAL):
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
        return TGEOGPOINT(MobilityDBReader.readTemporalType(TGEOGPOINT, value))


class TGEOGPOINTINST(TGEOGPOINT, TEMPORALINST):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALINST:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal instant")


class TGEOGPOINTI(TGEOGPOINT, TEMPORALI):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALI:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal instants")


class TGEOGPOINTSEQ(TGEOGPOINT, TEMPORALSEQ):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALSEQ:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal sequence")


class TGEOGPOINTS(TGEOGPOINT, TEMPORALS):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALS:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal sequences")
