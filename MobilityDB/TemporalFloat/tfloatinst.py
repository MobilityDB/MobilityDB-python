from MobilityDB.TemporalFloat.tfloat import TFLOAT
from MobilityDB.TemporalTypes.temporalinst import TEMPORALINST


class TFLOATINST(TFLOAT, TEMPORALINST):

    def __init__(self, value=None):
        super().__init__(value)
