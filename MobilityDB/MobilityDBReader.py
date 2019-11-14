from postgis.ewkb import Reader
import datetime
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
            return MobilityDBReader.readTemporalS(MainClass, value)
        elif '[' in value:
            MainClass.SubClass = TEMPORALSEQ
            return MobilityDBReader.readTemporalSeq(MainClass, value)
        elif '{' in value:
            MainClass.SubClass = TEMPORALI
            return MobilityDBReader.readTemporalI(MainClass, value)
        else:
            MainClass.SubClass = TEMPORALINST
            return MobilityDBReader.readTemporalInst(MainClass, value)

    @classmethod
    def readTemporalInst(cls, mainClass, valueStr=None):
        value = None
        inst = valueStr.split('@')
        if mainClass.BaseValueClass == Point:
            if '(' in inst[0] and ')' in inst[0]:
                value = cls.readPointFromString(inst[0])
            else:
                value = cls.from_hex(inst[0].strip())
        else:
            value = mainClass.BaseValueClass(inst[0])
        time = format(inst[1])
        return TEMPORALINST(value, time)

    @classmethod
    def readTemporalI(cls, mainClass, valueStr=None):
        valueStr = valueStr.replace('{', '')
        valueStr = valueStr.replace('}', '')
        instantsList = valueStr.split(',')
        # Parse every instant in the array
        instants = [cls.readTemporalInst(mainClass, instStr) for instStr in instantsList]
        return TEMPORALI(instants)

    @classmethod
    def readTemporalSeq(cls, mainClass, seqStr=None):
        seqStr = seqStr.replace('[', '')
        seqStr = seqStr.replace(']', '')
        instantsList = seqStr.split(',')
        # Parse every instant in the sequence
        instants = [cls.readTemporalInst(mainClass, instStr.strip()) for instStr in instantsList]
        return TEMPORALSEQ(instants)

    @classmethod
    def readTemporalS(cls, mainClass, inputValue=None):
        inputValue = inputValue.replace('{', '')
        inputValue = inputValue.replace('}', '')
        sequenceList = re.findall("(\[.+?\])+", inputValue)
        # Parse every sequence in the list
        instants = [cls.readTemporalSeq(mainClass, seq.strip()) for seq in sequenceList]
        return TEMPORALS(instants)

    @classmethod
    def readPointFromString(cls, valueStr=None):
        valueStr = valueStr.lower()
        nums = re.findall("[-+]?[0-9]*\.?[0-9]+", valueStr)
        return Point(nums)

    @classmethod
    def checkTemporalType(cls, value):
        # Check the temporal type and read it
        if '{' in value and '[' in value:
            return TEMPORALS
        elif '[' in value:
            return TEMPORALSEQ
        elif '{' in value:
            return TEMPORALI
        else:
            return TEMPORALINST
