from .tgeompoint import TGEOMPOINT
from MobilityDB.TemporalTypes.temporalinst import TEMPORALINST


class TGEOMPOINTINST(TGEOMPOINT, TEMPORALINST):

    def __init__(self, value=None):
        super().__init__(value)
