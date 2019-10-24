from MobilityDB.MobilityDBReader import MobilityDBTyped, MobilityDBReader


class TINT(object, metaclass=MobilityDBTyped):

    VALUECLASS = int

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TINT.CastTemporalTypes(value)

    @classmethod
    def CastTemporalTypes(cls, value):
        # Check the temporal type and read it
        if '[' in value:
            return MobilityDBReader.readTemporalSeq(MobilityDBTyped.types[7], value)
        else:
            return MobilityDBReader.readTemporalInst(MobilityDBTyped.types[5], value)
