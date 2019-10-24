from MobilityDB.TemporalGeometry.tgeompoint import TGEOMPOINT
from MobilityDB.Temporal.temporalseq import TEMPORALSEQ
from postgis import LineString


class TGEOMPOINTSEQ(TGEOMPOINT, TEMPORALSEQ):

    TYPE = 3
    MAINCLASS = TGEOMPOINT

    def getValue(self):
        return LineString([inst.value for inst in self.instants])
