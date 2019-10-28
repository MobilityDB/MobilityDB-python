from postgis.ewkb import Reader
from bdateutil.parser import parse
from postgis import Point
from MobilityDB.TemporalTypes import *
import re


# MobilityDBReader can read all the temporal types for all the base values based on the value of the data member
# "VALUECLASS" that is defined inside every class
class MobilityDBReader(Reader):

    @classmethod
    def readTemporalType(cls, MainClass, value):
        # Check the temporal type and read it
        if '{' in value and '[' in value:
            MainClass.SubClass = TEMPORALS
            return MobilityDBReader.readTemporalS(MainClass, TEMPORALS, value)
        elif '[' in value:
            MainClass.SubClass = TEMPORALSEQ
            return MobilityDBReader.readTemporalSeq(MainClass, TEMPORALSEQ, value)
        elif '{' in value:
            MainClass.SubClass = TEMPORALI
            return MobilityDBReader.readTemporalI(MainClass, TEMPORALI, value)
        else:
            MainClass.SubClass = TEMPORALINST
            return MobilityDBReader.readTemporalInst(MainClass, TEMPORALINST, value)

    @classmethod
    def readTemporalInst(cls, mainClass, temporalClass, valueStr=None):
        value = None
        inst = valueStr.split('@')
        if mainClass.BaseValueClass == Point:
            if '(' in inst[0] and ')' in inst[0]:
                value = cls.readPointFromString(inst[0])
            else:
                value = cls.from_hex(inst[0].strip())
        elif mainClass.BaseValueClass == int:
            value = int(inst[0])
        time = parse(inst[1])
        return temporalClass(value, time)

    @classmethod
    def readTemporalI(cls, mainClass, temporalClass, valueStr=None):
        instants = None
        valueStr = valueStr.replace('{', '')
        valueStr = valueStr.replace('}', '')
        instantsList = valueStr.split(',')
        # Parse every instant in the array
        if mainClass.BaseValueClass == Point:
            instants = [cls.readTemporalInst(mainClass, TEMPORALINST, instStr) for instStr in instantsList]
        elif mainClass.BaseValueClass == int:
            instants = [cls.readTemporalInst(mainClass, TEMPORALINST, instStr) for instStr in instantsList]
        return temporalClass(instants)

    @classmethod
    def readTemporalSeq(cls, mainClass, temporalClass, seqStr=None):
        instants = None
        seqStr = seqStr.replace('[', '')
        seqStr = seqStr.replace(']', '')
        instantsList = seqStr.split(',')
        # Parse every instant in the sequence
        if mainClass.BaseValueClass == Point:
            instants = [cls.readTemporalInst(mainClass, TEMPORALINST, instStr.strip()) for instStr in instantsList]
        elif mainClass.BaseValueClass == int:
            instants = [cls.readTemporalInst(mainClass, TEMPORALINST, instStr.strip()) for instStr in instantsList]
        return temporalClass(instants)

    @classmethod
    def readTemporalS(cls, mainClass, temporalClass, inputValue=None):
        instants = None
        inputValue = inputValue.replace('{', '')
        inputValue = inputValue.replace('}', '')
        sequenceList = re.findall("(\[.+?\])+", inputValue)

        # Parse every sequence in the list
        if mainClass.BaseValueClass == Point:
            instants = [cls.readTemporalSeq(mainClass, TEMPORALSEQ, seq.strip()) for seq in sequenceList]
        elif mainClass.BaseValueClass == int:
            instants = [cls.readTemporalSeq(mainClass, TEMPORALSEQ, seq.strip()) for seq in sequenceList]
        return temporalClass(instants)

    @classmethod
    def readPointFromString(cls, valueStr=None):
        valueStr = valueStr.lower()
        valueStr = valueStr.replace("point(", "")
        valueStr = valueStr.replace(")", "")
        num = valueStr.split(" ")
        if len(num) == 2:
            return Point(num[0], num[1])
        elif len(num) == 3:
            return Point(num[0], num[1], num[3])
