from MobilityDB.TemporalFloat.tfloat import TFLOAT
from MobilityDB.TemporalTypes.temporali import TEMPORALI


class TFLOATI(TFLOAT, TEMPORALI):

    def __init__(self, value=None):
        super().__init__(value)
