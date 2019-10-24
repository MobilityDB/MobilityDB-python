from MobilityDB.TemporalGeometry.tgeompoint import TGEOMPOINT
from MobilityDB.Temporal.temporali import TEMPORALI


class TGEOMPOINTI(TGEOMPOINT, TEMPORALI):

    TYPE = 2
    MAINCLASS = TGEOMPOINT
