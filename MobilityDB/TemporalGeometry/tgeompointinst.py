from MobilityDB.TemporalGeometry.tgeompoint import TGEOMPOINT
from MobilityDB.Temporal.temporalinst import TEMPORALINST

class TGEOMPOINTINST(TGEOMPOINT, TEMPORALINST):

    TYPE = 1
    MAINCLASS = TGEOMPOINT
