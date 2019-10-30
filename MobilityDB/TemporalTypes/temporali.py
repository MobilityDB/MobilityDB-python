from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS


class TEMPORALI(TEMPORALINSTANTS):
    Duration = 2

    @classmethod
    def getType(cls):
        return "InstantSet"

    def __str__(self):
        return "{}'{{{}}}'".format("", self.getInstants())
