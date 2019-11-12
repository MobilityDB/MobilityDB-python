from MobilityDB.TemporalInteger.tint import TINT
from MobilityDB.TemporalTypes.temporali import TEMPORALI


class TINTI(TINT, TEMPORALI):

    def __init__(self, value=None):
        super().__init__(value)
