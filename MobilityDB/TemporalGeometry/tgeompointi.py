from MobilityDB.TemporalGeometry.tgeompoint import TGEOMPOINT
from MobilityDB.TemporalTypes.temporali import TEMPORALI


class TGEOMPOINTI(TGEOMPOINT, TEMPORALI):

    def __init__(self, value=None):
        super().__init__(value)
