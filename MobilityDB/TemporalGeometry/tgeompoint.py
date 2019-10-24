from MobilityDB.MobilityDBReader import MobilityDBTyped, MobilityDBReader
from postgis import Point


class TGEOMPOINT(object, metaclass=MobilityDBTyped):

    VALUECLASS = Point

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TGEOMPOINT.CastTemporalTypes(value)

    @classmethod
    def CastTemporalTypes(cls, value):
        # Check the temporal type and read it
        if '[' in value:
            return MobilityDBReader.readTemporalSeq(MobilityDBTyped.types[3], value)
        elif '{' in value:
            return MobilityDBReader.readTemporalI(MobilityDBTyped.types[2], value)
        else:
            return MobilityDBReader.readTemporalInst(MobilityDBTyped.types[1], value)
