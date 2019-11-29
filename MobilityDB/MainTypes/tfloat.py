from MobilityDB.TemporalTypes import *
from spans.types import Range


class floatrange(Range):
	__slots__ = ()
	type = float

class TFloat(Temporal):
	BaseValueClass = float
	ComponentValueClass = None

	def __init__(self, value):
		if isinstance(value, str):
			subclasses = self.__class__.__subclasses__()
			print(subclasses)
			if value[0] != '{' and value[0] != '[' and value[0] != '(':
				# TemporalInst
				subclasses[0](value)
			elif value[0] == '[' or value[0] == '(':
				# TemporalSeq
				subclasses[2](value)
			elif (value[0] == '{'):
				# TemporalS
				if value[1] == '[' or value[1] == '(':
					subclasses[3](value)
				else:
					# TemporalS
					subclasses[1](value)
		else:
			raise Exception("ERROR: Could not parse temporal value")

	def valueRange(self):
		"""
		Distinct values
		"""
		return floatrange(self.minValue(), self.maxValue(), True, True)

	def __str__(self):
		"""
		String representation
		"""
		print(type(self))
		pass

class TFloatInst(TemporalInst, TFloat):

	def __init__(self, value, time=None):
		TemporalInst.BaseValueClass = float
		super().__init__(value, time)

	def getValues(self):
		"""
		Distinct values
		"""
		return floatrange(self._value, self._value, True, True)

class TFloatI(TemporalI, TFloat):

	def __init__(self,  *argv):
		TemporalI.BaseValueClass = float
		TemporalI.ComponentValueClass = TFloatInst
		super().__init__(*argv)

	def getValues(self):
		"""
		Distinct values
		"""
		values = super().getValues()
		return [floatrange(value, value, True, True) for value in values]

class TFloatSeq(TemporalSeq, TFloat):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseValueClass = float
		TemporalSeq.ComponentValueClass = TFloatInst
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

class TFloatS(TemporalS, TFloat):

	def __init__(self, *argv):
		TemporalS.BaseValueClass = float
		TemporalS.ComponentValueClass = TFloatSeq
		super().__init__(*argv)

	def getValues(self):
		"""
		Distinct values
		"""
		ranges = sorted([seq.getValues() for seq in self._sequenceList])
		# Normalize list of ranges
		result = []
		range = ranges[0]
		for range1 in ranges[1:]:
			if range.adjacent(range1) or range.overlap(range1):
				range = range.union(range1)
			else:
				result.append(range)
				range = range1
		result.append(range)
		return result

