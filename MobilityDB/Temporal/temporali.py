from MobilityDB.Temporal.composedInstants import COMPOSEDTEMPORALINST


class TEMPORALI(COMPOSEDTEMPORALINST):

    def __str__(self):
        return self.MAINCLASS.__name__ + "(INSTANTSET)'{" + self.getinstants()+"}'"
