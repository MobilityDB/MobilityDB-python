from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS
from postgis import LineString


class TEMPORALSEQ(TEMPORALINSTANTS):
    Duration = 3

    @classmethod
    def getType(cls):
        return "Sequence"

    def __str__(self):
        return "{}'[{}]'".format("(Sequence)", self.getinstants())
