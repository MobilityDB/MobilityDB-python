from .tgeompoint import TGEOMPOINT
from MobilityDB.TemporalTypes.temporals import TEMPORALS


class TGEOMPOINTS(TGEOMPOINT, TEMPORALS):

    def __init__(self, value=None):
        super().__init__(value)
