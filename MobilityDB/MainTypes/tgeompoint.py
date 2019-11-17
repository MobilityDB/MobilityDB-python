from postgis import Point
from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TGEOMPOINT(TEMPORAL):
    BaseValueClass = Point
    SRID = 0

    def __init__(self, value=None, srid=None):
        if isinstance(value, str):
            self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
            if srid is not None:
                self.SRID = srid
            else:
                self.SRID = 0
        elif isinstance(value, list):
            try:
                instants = []
                for item in value:
                    if isinstance(item, self.SubClass.__class__.__bases__[0]):
                        instants.append(item)
                self.SubClass = TEMPORALI(instants)
            except:
                raise Exception("ERROR: different types")
        else:
            self.SubClass = value

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TGEOMPOINT(MobilityDBReader.readTemporalType(TGEOMPOINT, value))

    def __str__(self):
        if len(self.__class__.__bases__) == 2:
            return self.__class__.__bases__[0].__name__ + " 'SRID=" + str(
                self.SRID) + ";" + self.SubClass.__str__() + "'"
        else:
            return self.__class__.__name__ + " 'SRID=" + str(self.SRID) + ";" + self.SubClass.__str__() + "'"


class TGEOMPOINTINST(TGEOMPOINT, TEMPORALINST):

    def __init__(self, value=None, srid=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALINST:
            super().__init__(value, srid)
        else:
            raise Exception("ERROR: Input must be a temporal instant")


class TGEOMPOINTI(TGEOMPOINT, TEMPORALI):

    def __init__(self, value=None, srid=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALI or isinstance(value, list):
            super().__init__(value, srid)
        else:
            raise Exception("ERROR: Input must be a temporal instants")


class TGEOMPOINTSEQ(TGEOMPOINT, TEMPORALSEQ):

    def __init__(self, value=None, srid=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALSEQ:
            super().__init__(value, srid)
        else:
            raise Exception("ERROR: Input must be a temporal sequence")


class TGEOMPOINTS(TGEOMPOINT, TEMPORALS):

    def __init__(self, value=None, srid=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALS:
            super().__init__(value, srid)
        else:
            raise Exception("ERROR: Input must be a temporal sequences")
