from MobilityDB.TemporalInteger.tint import TINT
from MobilityDB.Temporal.temporalinst import TEMPORALINST


class TINTINST(TINT, TEMPORALINST):

    TYPE = 5
    MAINCLASS = TINT
