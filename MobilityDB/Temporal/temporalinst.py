from MobilityDB.MobilityDBReader import MobilityDBReader
from bdateutil.parser import parse

class TEMPORALINST:

    __slots__ = ['value', 'time']
    MAINCLASS = None

    def __init__(self, value=None, time=None):
        if isinstance(value, self.MAINCLASS.VALUECLASS):
            self.value = value
            self.time = time
        elif isinstance(value, str):
            inst = value.split('@')
            self.value = MobilityDBReader.readPointFromString(inst[0])
            self.time = parse(inst[1])

    def getValue(self):
        return self.value

    def getTimestamp(self):
        return self.time

    def __str__(self):
        return self.MAINCLASS.__name__+"(instant)" + "'" + self.value.__str__() + "@" + self.time.__str__() + "'"
