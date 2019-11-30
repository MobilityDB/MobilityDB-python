from spans.types import Range
from MobilityDB.TemporalTypes import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class floatrange(Range):
	__slots__ = ()
	type = float

class TFloat(Temporal):
	"""
	Temporal floats of any duration (abstract class)
	"""
	Interpolation = 'linear'

	def valueRange(self):
		"""
		Distinct values
		"""
		return floatrange(self.minValue(), self.maxValue(), True, True)

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TFloatInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TFloatSeq(value)
		elif value[0] == '{':
			if value[1] == '[' or value[1] == '(':
				return TFloatS(value)
			else:
				return TFloatI(value)
		raise Exception("ERROR: Could not parse temporal float value")

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

class TFloatInst(TemporalInst, TFloat):
	"""
	Temporal floats of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = float
		super().__init__(value, time)

	def getValues(self):
		"""
		Distinct values
		"""
		return floatrange(self._value, self._value, True, True)


class TFloatI(TemporalI, TFloat):
	"""
	Temporal floats of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = float
		TemporalI.ComponentClass = TFloatInst
		super().__init__(*argv)

	def getValues(self):
		"""
		Distinct values
		"""
		values = super().getValues()
		return [floatrange(value, value, True, True) for value in values]


class TFloatSeq(TemporalSeq, TFloat):
	"""
	Temporal floats of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseClass = float
		TemporalSeq.ComponentClass = TFloatInst
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
	"""
	Temporal floats of sequence set duration
	"""
	def __init__(self, *argv):
		TemporalS.BaseClass = float
		TemporalS.ComponentClass = TFloatSeq
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
