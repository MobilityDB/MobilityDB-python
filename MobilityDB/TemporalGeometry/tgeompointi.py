from MobilityDB.TemporalGeometry.tgeompoint import TGEOMPOINT
from MobilityDB.TemporalTypes.temporali import TEMPORALI


class TGEOMPOINTI(TGEOMPOINT, TEMPORALI):

    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        print(self.SubClass.value.__str__())
        return self.__class__.__bases__[0].__name__+self.SubClass.__str__()
