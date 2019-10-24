from MobilityDB.TemporalInteger.tint import TINT
from MobilityDB.Temporal.temporalseq import TEMPORALSEQ


class TINTSEQ(TINT, TEMPORALSEQ):

    TYPE = 7
    MAINCLASS = TINT
