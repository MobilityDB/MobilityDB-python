from postgis.ewkb import Reader
from bdateutil.parser import parse
from postgis import Point


class MobilityDBTyped(type):
    types = {}

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        if hasattr(cls, 'TYPE'):
            MobilityDBTyped.types[cls.TYPE] = cls
        return cls

    def __call__(cls, *args, **kwargs):
        # Allow to pass an instance as first argument, for blind casting.
        if args and isinstance(args[0], cls):
            return args[0]
        return super().__call__(*args, **kwargs)


# MobilityDBReader can read all the temporal types for all the base values based on the value of the data member
# "VALUECLASS" that is defined inside every class.
class MobilityDBReader(Reader):

    @classmethod
    def readTemporalInst(cls, temporalClass_, valueStr=None):
        inst = valueStr.split('@')
        if temporalClass_.VALUECLASS == Point:
            if '(' in inst[0] and ')' in inst[0]:
                value = cls.readPointFromString(inst[0])
            else:
                value = cls.from_hex(inst[0].strip())
        elif temporalClass_.VALUECLASS == int:
            value = int(inst[0])
        time = parse(inst[1])
        return temporalClass_(value, time)

    @classmethod
    def readTemporalI(cls, temporalClass_, valueStr=None):
        valueStr = valueStr.replace('{', '')
        valueStr = valueStr.replace('}', '')
        instantsList = valueStr.split(',')
        instants = None
        # Parse every instant in the array
        if temporalClass_.VALUECLASS == Point:
            instants = [cls.readTemporalInst(MobilityDBTyped.types[1], instStr) for instStr in instantsList]
        elif temporalClass_.VALUECLASS == int:
            instants = [cls.readTemporalInst(MobilityDBTyped.types[5], instStr) for instStr in instantsList]
        return temporalClass_(instants)

    @classmethod
    def readTemporalSeq(cls, temporalClass_, seqStr=None):
        seqStr = seqStr.replace('[', '')
        seqStr = seqStr.replace(']', '')
        instantsList = seqStr.split(',')
        instants = None
        # Parse every instant in the sequence
        if temporalClass_.VALUECLASS == Point:
            instants = [cls.readTemporalInst(MobilityDBTyped.types[1], instStr.strip()) for instStr in instantsList]
        elif temporalClass_.VALUECLASS == int:
            instants = [cls.readTemporalInst(MobilityDBTyped.types[5], instStr.strip()) for instStr in instantsList]
        return temporalClass_(instants)

    @classmethod
    def readPointFromString(cls, valueStr=None):
        valueStr = valueStr.replace("point(", "")
        valueStr = valueStr.replace(")", "")
        num = valueStr.split(" ")
        if len(num) == 2:
            return Point(num[0], num[1])
        elif len(num) == 3:
            return Point(num[0], num[1], num[3])
