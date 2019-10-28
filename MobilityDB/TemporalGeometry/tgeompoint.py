from postgis import Point
from MobilityDB.TemporalTypes.temporal import TEMPORAL
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
        return self.__class__.__name__ + self.SubClass.__str__()
