from MobilityDB.TimeTypes import *


class TEMPORAL:
    BaseValueClass = None
    SubClass = None

    # Accessor functions
    def getValue(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.value
        raise Exception("ERROR: Input must be a temporal instant")

    def getValues(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.value
        elif self.SubClass.Duration == 2:
            return [inst.value for inst in self.SubClass.value]
        elif self.SubClass.Duration == 3:
            return self.SubClass.getDistinctValues(self.BaseValueClass)

    def getTimestamp(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.time
        raise Exception("ERROR: Input must be a temporal instant")

    def timespan(self):
        if self.SubClass.Duration == 2:
            return PERIOD(min(inst.time for inst in self.SubClass.value),
                          max(inst.time for inst in self.SubClass.value))
        if self.SubClass.Duration == 3:
            return PERIOD(self.startInstant().time, self.endInstant().time)

    def startInstant(self):
        if self.SubClass.Duration == 1:
            return self.SubClass
        elif self.SubClass.Duration in [2, 3]:
            return self.SubClass.startInstant()
        else:
            raise Exception("ERROR:  Could not parse temporal value")

    def endInstant(self):
        if self.SubClass.Duration == 1:
            return self.SubClass
        elif self.SubClass.Duration in [2, 3]:
            return self.SubClass.endInstant()
        else:
            raise Exception("ERROR:  Could not parse temporal value")

    def startValue(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.value
        elif self.SubClass.Duration in [2, 3]:
            return self.SubClass.startInstant().value

    def endValue(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.value
        elif self.SubClass.Duration in [2, 3]:
            return self.SubClass.endInstant().value

    def getType(self):
        if self.SubClass.Duration == 1:
            return "Instant"
        elif self.SubClass.Duration == 2:
            return "InstantSet"
        elif self.SubClass.Duration == 3:
            return "Sequence"

    def instantN(self, n):
        if self.SubClass.Duration == 1 and n == 1:
            return self.SubClass
        elif self.SubClass.Duration in [2, 3] and 0 < n < self.SubClass.numInstants():
            return self.SubClass.value[n - 1]
        else:
            raise Exception("ERROR: there is no value at this index")

    def sequenceN(self, n):
        if 0 <= n < self.SubClass.numSequences():
            return self.SubClass.sequences[n]
        raise Exception("ERROR: out of range")

    # Comparison is missing
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return True

    def __str__(self):
        if len(self.__class__.__bases__) == 2:
            return self.__class__.__bases__[0].__name__ + " '"+self.SubClass.__str__()+"'"
        else:
            return self.__class__.__name__ + " '"+self.SubClass.__str__()+"'"
