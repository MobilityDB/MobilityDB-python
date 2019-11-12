from MobilityDB.TemporalFloat.tfloat import TFLOAT
from MobilityDB.TemporalTypes.temporals import TEMPORALS


class TFLOATS(TFLOAT, TEMPORALS):

    def __init__(self, value=None):
        super().__init__(value)
