from MobilityDB.TimeTypes.period import PERIOD
from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS


class TEMPORALSEQ(TEMPORALINSTANTS):
	__slots__ = ['_lower_inc', '_upper_inc']
	Duration = 3

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TEMPORALINSTANTS.__init__(self, instantList)
		self._lower_inc = lower_inc if lower_inc is not None else True
		self._upper_inc = upper_inc if upper_inc is not None else True
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: Invalid bounds for temporal sequence value")

	def _valid(self):
		return len(self._instantList) > 1 or (self._lower_inc and self._lower_inc)

	@classmethod
	def duration(cls):
		return "Sequence"

	def lower_inc(self):
		"""
		Is the lower bound of the temporal sequence inclusive?
		"""
		return self._lower_inc

	def upper_inc(self):
		"""
		Is the upper bound of the temporal sequence inclusive?
		"""
		return self._upper_inc

	def period(self):
		"""
		Period on which the temporal value is defined
		"""
		return PERIOD(self.startTimestamp(), self.endTimestamp(), self.lower_inc(), self.upper_inc())

	def numSequences(self):
		"""
		Number of sequences
		"""
		return 1

	def startSequence(self):
		"""
		Start sequence
		"""
		return self

	def endSequence(self):
		"""
		End sequence
		"""
		return self

	def sequenceN(self, n):
		"""
		N-th sequence
		"""
		# 1-based
		if n == 1:
			return self
		else:
			raise Exception("ERROR: Out of range")

	def sequences(self):
		"""
		Sequences
		"""
		return [self]

	def distinctValues(self, base=None):
		"""
		Distinct values
		"""
		valueList = []
		for inst in self._instantList:
			valueList.append(inst._value)
		# Remove duplicates
		valueList = list(dict.fromkeys(valueList))
		return valueList

	def __str__(self):
		lower_str = '[' if self._lower_inc else '('
		upper_str = ']' if self._upper_inc else ')'
		return lower_str + 	TEMPORALINSTANTS.__str__(self) + upper_str

