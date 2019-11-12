from MobilityDB.TemporalInteger.tint import TINT
from MobilityDB.TemporalTypes.temporalinst import TEMPORALINST


class TINTINST(TINT, TEMPORALINST):

    def __init__(self, value=None):
        super().__init__(value)
