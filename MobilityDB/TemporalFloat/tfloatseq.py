from MobilityDB.TemporalFloat.tfloat import TFLOAT
from MobilityDB.TemporalTypes.temporalseq import TEMPORALSEQ


class TFLOATSEQ(TFLOAT, TEMPORALSEQ):

    def __init__(self, value=None):
        super().__init__(value)
