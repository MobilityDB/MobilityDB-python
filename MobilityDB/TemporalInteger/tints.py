from MobilityDB.TemporalInteger.tint import TINT
from MobilityDB.TemporalTypes.temporals import TEMPORALS


class TINTS(TINT, TEMPORALS):

    def __init__(self, value=None):
        super().__init__(value)
