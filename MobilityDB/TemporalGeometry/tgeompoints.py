from .tgeompoint import TGEOMPOINT
from MobilityDB.TemporalTypes.temporals import TEMPORALS


class TGEOMPOINTS(TGEOMPOINT, TEMPORALS):

    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return self.__class__.__bases__[0].__name__+self.SubClass.__str__()
