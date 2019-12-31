from parsec import *
from MobilityDB.TemporalTypes.temporal_parser import *
from MobilityDB.TimeTypes.period import Period
from MobilityDB.TimeTypes.periodset import PeriodSet
from MobilityDB.TemporalTypes.temporalinst import TemporalInst
from MobilityDB.TemporalTypes.temporalinstants import TemporalInstants

class TemporalSeq(TemporalInstants):
	"""
	Abstract class for temporal types of sequence duration
	"""
	__slots__ = ['_lower_inc', '_upper_inc', '_interp']

	def __init__(self, instantList, lower_inc=None, upper_inc=None, interp=None):
		assert(isinstance(lower_inc, (bool, type(None))))
		assert(isinstance(upper_inc, (bool, type(None))))
		self._instantList = []
		# Constructor with a single argument of type string
		if isinstance(instantList, str):
			elements = parse_temporalseq(instantList, 0)
			print(elements)
			for inst in elements[2][0]:
				self._instantList.append(TemporalSeq.ComponentClass(inst[0], inst[1]))
			self._lower_inc = elements[2][1]
			self._upper_inc = elements[2][2]
			# Set interpolation with the argument value if given
			self._interp = interp if interp is not None else elements[2][3]
		# Constructor with a first argument of type list and optional arguments for the bounds and interpolation
		elif isinstance(instantList, list):
			# List of strings representing instant values
			if all(isinstance(arg, str) for arg in instantList):
				for arg in instantList:
					self._instantList.append(TemporalSeq.ComponentClass(arg))
			# List of instant values
			elif all(isinstance(arg, TemporalSeq.ComponentClass) for arg in instantList):
				for arg in instantList:
					self._instantList.append(arg)
			else:
				raise Exception("ERROR: Could not parse temporal sequence value")
			self._lower_inc = lower_inc if lower_inc is not None else True
			self._upper_inc = upper_inc if upper_inc is not None else False
			if interp is None or interp == 'Linear':
				self._interp = 'Linear'
			elif interp == 'Stepwise':
				self._interp = 'Stepwise'
			else:
				raise Exception("ERROR: Invalid interpolation")
		else:
			raise Exception("ERROR: Could not parse temporal sequence value")
		# Verify validity of the resulting instance
		self._valid()

	def _valid(self):
		if len(self._instantList) == 1 and (not self._lower_inc or not self._lower_inc):
			raise Exception("ERROR: The lower and upper bounds must be inclusive for an instant temporal sequence")
		if any(x._time >= y._time for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: The timestamps of a temporal sequence must be increasing")
		if (self._interp == 'Stepwise' and len(self._instantList) > 1 and not self._upper_inc and
			self._instantList[-1]._value != self._instantList[-2]._value):
			raise Exception("ERROR: The last two values of a temporal sequence with exclusive upper bound and stepwise interpolation must be equal")
		return True

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

	def getTime(self):
		"""
		Period set on which the temporal value is defined
		"""
		return PeriodSet([self.period()])

	def period(self):
		"""
		Period on which the temporal value is defined ignoring potential time gaps
		"""
		return Period(self.startTimestamp(), self.endTimestamp(), self.lower_inc(), self.upper_inc())

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

	def intersectsTimestamp(self, timestamp):
		"""
		Intersects timestamp?
		"""
		return ((self.lower_inc and self._instantList[0]._time == timestamp) or
			(self.upper_inc and self._instantList[-1]._time == timestamp) or
			(self._instantList[0]._time < timestamp < self._instantList[-1]._time))

	def intersectsTimestampset(self, timestampset):
		"""
		Intersects timestamp set?
		"""
		return any(self.intersectsTimestamp(timestamp) for timestamp in timestampset._datetimeList)

	def intersectsPeriod(self, period):
		"""
		Intersects period?
		"""
		return self.period().overlap(period)

	def intersectsPeriodset(self, periodset):
		"""
		Intersects period set?
		"""
		return any(self.intersectsPeriod(period) for period in periodset._periodList)

	# Comparisons are missing
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._instantList == other._instantList and self._lower_inc == other._lower_inc and \
				self._upper_inc == other._upper_inc and self._interp == other._interp:
				return True
		return False

	def __str__(self):
		lower_str = '[' if self._lower_inc else '('
		upper_str = ']' if self._upper_inc else ')'
		return (f"'{lower_str}{TemporalInstants.__str__(self)}{upper_str}'")

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._instantList!r}, {self._lower_inc!r}, {self._upper_inc!r}, {self._interp!r})')