from postgis import Point, LineString


class TEMPORAL:
    BaseValueClass = None
    SubClass = None

    def getValue(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.value
        raise Exception("ERROR: Input must be a temporal instant")

    def getValues(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.value
        elif self.SubClass.Duration == 2:
            return self.SubClass.value
        elif self.SubClass.Duration == 3:
            return LineString([inst.value for inst in self.SubClass.value])

    def getTimestamp(self):
        if self.SubClass.Duration == 1:
            return self.SubClass.time
        raise Exception("ERROR: Input must be a temporal instant")

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

