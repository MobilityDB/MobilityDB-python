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
			MainClass.SubClass = TemporalS
			return MobilityDBReader.readTemporalS(MainClass, value)
		elif '[' in value:
			MainClass.SubClass = TemporalSeq
			return MobilityDBReader.readTemporalSeq(MainClass, value)
		elif '{' in value:
			MainClass.SubClass = TemporalI
			return MobilityDBReader.readTemporalI(MainClass, value)
		else:
			MainClass.SubClass = TemporalInst
			return MobilityDBReader.readTemporalInst(MainClass, value)

	@classmethod
	def readTemporalInst(cls, mainClass, valueStr=None):
		value = None
		inst = valueStr.split('@')
		if mainClass.BaseClass == Point:
			if '(' in inst[0] and ')' in inst[0]:
				value = cls.readPointFromString(inst[0])
			else:
				value = cls.from_hex(inst[0].strip())
		else:
			value = mainClass.BaseClass(inst[0])
		time = format(inst[1])
		return TemporalInst(value, time)

	@classmethod
	def readTemporalI(cls, mainClass, valueStr=None):
		valueStr = valueStr.replace('{', '')
		valueStr = valueStr.replace('}', '')
		instantList = valueStr.split(',')
		# Parse every instant in the array
		instants = [cls.readTemporalInst(mainClass, instStr) for instStr in instantList]
		return TemporalI(instants)

	@classmethod
	def readTemporalSeq(cls, mainClass, seqStr=None):
		seqStr = seqStr.replace('[', '')
		seqStr = seqStr.replace(']', '')
		instantsList = seqStr.split(',')
		# Parse every instant in the sequence
		instants = [cls.readTemporalInst(mainClass, instStr.strip()) for instStr in instantsList]
		return TemporalSeq(instants)

	@classmethod
	def readTemporalS(cls, mainClass, inputValue=None):
		inputValue = inputValue.replace('{', '')
		inputValue = inputValue.replace('}', '')
		sequenceList = re.findall("(\[.+?\])+", inputValue)
		# Parse every sequence in the list
		instants = [cls.readTemporalSeq(mainClass, seq.strip()) for seq in sequenceList]
		return TemporalS(instants)

	@classmethod
	def readPointFromString(cls, valueStr=None):
		valueStr = valueStr.lower()
		nums = re.findall("[-+]?[0-9]*\.?[0-9]+", valueStr)
		return Point(nums)

	@classmethod
	def checkTemporalType(cls, value):
		# Check the temporal type and read it
		if '{' in value and '[' in value:
			return TemporalS
		elif '[' in value:
			return TemporalSeq
		elif '{' in value:
			return TemporalI
		else:
			return TemporalInst
