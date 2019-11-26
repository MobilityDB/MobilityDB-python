from MobilityDB.TemporalTypes import *
from spans.types import Range

class floatrange(Range):
	__slots__ = ()
	type = float

class TFLOAT(TEMPORAL):
	BaseValueClass = float
	ComponentValueClass = None

	def valueRange(self):
		"""
		Distinct values
		"""
		return floatrange(self.minValue(), self.maxValue(), True, True)

class TFLOATINST(TEMPORALINST, TFLOAT):

	def __init__(self, value, time=None):
		super().__init__(value, time)
		TEMPORALINST.BaseValueClass = float

class TFLOATI(TEMPORALI, TFLOAT):

	def __init__(self,  *argv):
		TEMPORALI.BaseValueClass = float
		TEMPORALI.ComponentValueClass = TFLOATINST
		super().__init__(*argv)

	def getValues(self):
		"""
		Distinct values
		"""
		values = super().getValues()
		return [floatrange(value, value, True, True) for value in values]

class TFLOATSEQ(TEMPORALSEQ, TFLOAT):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TEMPORALSEQ.BaseValueClass = float
		TEMPORALSEQ.ComponentValueClass = TFLOATINST
		super().__init__(instantList, lower_inc, upper_inc)

	def getValues(self):
		"""
		Distinct values
		"""
		min = self.minValue()
		max = self.maxValue()
		lower = self.startValue()
		upper = self.endValue()
		min_inc = min < lower or (min == lower and self.lower_inc)
		max_inc = max > upper or (max == upper and self.upper_inc)
		if not min_inc:
			min_inc = min in self._instantList[1:-1]
		if not max_inc:
			max_inc = max in self._instantList[1:-1]
		return floatrange(min, max, min_inc, max_inc)

class TFLOATS(TEMPORALS, TFLOAT):

	def __init__(self, *argv):
		TEMPORALS.BaseValueClass = float
		TEMPORALS.ComponentValueClass = TFLOATSEQ
		super().__init__(*argv)

	def getValues(self):
		"""
		Distinct values
		"""
		ranges = [seq.getValues() for seq in self._sequenceList]
		print("*****")
		print(ranges)
		print(ranges[0] < ranges[1])
		print("*****")
		print(ranges.sort())
		return floatrange(self.minValue(), self.maxValue())

