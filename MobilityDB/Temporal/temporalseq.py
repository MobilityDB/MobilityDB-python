from MobilityDB.Temporal.composedInstants import COMPOSEDTEMPORALINST


class TEMPORALSEQ(COMPOSEDTEMPORALINST):

    # def timespan(self)

    def __str__(self):
        return self.MAINCLASS.__name__ + "(SEQUENCE)'[" + self.getinstants()+"]'"
