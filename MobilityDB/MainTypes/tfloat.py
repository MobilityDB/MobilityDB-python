from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TFLOAT(TEMPORAL):
    BaseValueClass = float

    def __init__(self, value=None):
        if isinstance(value, str):
            self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
        elif isinstance(value, list):
            try:
                listItems = []
                for item in value:
                    if isinstance(item, self.SubClass.__class__.__bases__[0]):
                        listItems.append(item.SubClass)
                if value[0].SubClass.__class__ == TEMPORALINST:
                    self.SubClass = TEMPORALI(listItems)
                elif value[0].SubClass.__class__ == TEMPORALSEQ:
                    self.SubClass = TEMPORALS(listItems)
            except:
                raise Exception("ERROR: different types")
        else:
            self.SubClass = value

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TFLOAT(MobilityDBReader.readTemporalType(TFLOAT, value))


class TFLOATINST(TFLOAT, TEMPORALINST):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALINST:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal instant")


class TFLOATI(TFLOAT, TEMPORALI):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALI or isinstance(value, list):
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal instants")


class TFLOATSEQ(TFLOAT, TEMPORALSEQ):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALSEQ:
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal sequence")


class TFLOATS(TFLOAT, TEMPORALS):

    def __init__(self, value=None):
        if MobilityDBReader.checkTemporalType(value) == TEMPORALS or isinstance(value, list):
            super().__init__(value)
        else:
            raise Exception("ERROR: Input must be a temporal sequences")
