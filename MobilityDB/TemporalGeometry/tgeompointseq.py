from .tgeompoint import TGEOMPOINT
from MobilityDB.TemporalTypes.temporalseq import TEMPORALSEQ


class TGEOMPOINTSEQ(TGEOMPOINT, TEMPORALSEQ):

    def __init__(self, value=None):
        super().__init__(value)
