from MobilityDB.TemporalInteger.tint import TINT
from MobilityDB.TemporalTypes.temporalseq import TEMPORALSEQ


class TINTSEQ(TINT, TEMPORALSEQ):

    def __init__(self, value=None):
        super().__init__(value)
