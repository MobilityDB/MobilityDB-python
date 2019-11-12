from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TBOOL(TEMPORAL):
    BaseValueClass = bool

    def __init__(self, value=None):
        if isinstance(value, str):
            self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
        else:
            self.SubClass = value

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBOOL(MobilityDBReader.readTemporalType(TBOOL, value))

    def __str__(self):
        if len(self.__class__.__bases__) == 2:
            return self.__class__.__bases__[0].__name__ + self.SubClass.__str__()
        else:
            return self.__class__.__name__ + self.SubClass.__str__()


class TBOOLINST(TBOOL, TEMPORALINST):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALINST:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal instant")


class TBOOLI(TBOOL, TEMPORALI):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALI:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal instants")


class TBOOLSEQ(TBOOL, TEMPORALSEQ):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALSEQ:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal sequence")


class TBOOLS(TBOOL, TEMPORALS):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALS:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal sequences")
