from mobilitydb.time import Period, PeriodSet
from mobilitydb.temporal.temporal import Temporal
from mobilitydb.temporal.temporal_parser import parse_temporals


class TemporalS(Temporal):
	"""
	Abstract class for temporal types of sequence set duration
	"""
	__slots__ = ['_sequenceList', '_interp']

	def __init__(self, sequenceList, interp=None):
		assert (isinstance(interp, (str, type(None)))), "ERROR: Invalid interpolation"
		if isinstance(interp, str) and interp is None:
			assert (interp == 'Linear' or interp == 'Stepwise'), "ERROR: Invalid interpolation"
		self._sequenceList = []
		# Constructor with a single argument of type string
		if isinstance(sequenceList, str):
			elements = parse_temporals(sequenceList, 0)
			seqList = []
			for seq in elements[2][0]:
				instList = []
				for inst in seq[0]:
					instList.append(TemporalS.ComponentClass.ComponentClass(inst[0], inst[1]))
				if self.__class__.BaseClassDiscrete:
					seqList.append(TemporalS.ComponentClass(instList, seq[1], seq[2]))
				else:
					seqList.append(TemporalS.ComponentClass(instList, seq[1], seq[2], elements[2][1]))
			self._sequenceList = seqList
			# Set interpolation with the argument or the flag from the string if given
			if interp is not None:
				self._interp = interp
			else:
				if self.__class__.BaseClassDiscrete:
					self._interp = 'Stepwise'
				else:
					self._interp = elements[2][1] if elements[2][1] is not None else 'Linear'
		# Constructor with a single argument of type list
		elif isinstance(sequenceList, list):
			# List of strings representing periods
			if all(isinstance(sequence, str) for sequence in sequenceList):
				for sequence in sequenceList:
					self._sequenceList.append(self.__class__.ComponentClass(sequence))
			# List of periods
			elif all(isinstance(sequence, self.__class__.ComponentClass) for sequence in sequenceList):
				for sequence in sequenceList:
					self._sequenceList.append(sequence)
			else:
				raise Exception("ERROR: Could not parse temporal sequence set value")
			# Set the interpolation
			if interp is not None:
				self._interp = interp
			else:
				self._interp = 'Stepwise' if self.__class__.BaseClassDiscrete else 'Linear'
		else:
			raise Exception("ERROR: Could not parse temporal sequence set value")
		# Verify validity of the resulting instance
		self._valid()

	def _valid(self):
		if any(x.endTimestamp() >= y.startTimestamp() or \
					   (x.endTimestamp() == y.startTimestamp() and x.upper_inc() and x.lower_inc()) \
			   for x, y in zip(self._sequenceList, self._sequenceList[1:])):
			raise Exception("ERROR: The sequences of a sequence set cannot overlap")
		if any(x.interpolation() != y.interpolation() \
			   for x, y in zip(self._sequenceList, self._sequenceList[1:])):
			raise Exception("ERROR: All sequences of a sequence set must have the same interpolation")
		return True

	@classmethod
	def duration(cls):
		return "SequenceSet"

	def getValues(self):
		"""
		Distinct values
		"""
		values = [seq.getValues() for seq in self._sequenceList]
		return list(dict.fromkeys([item for sublist in values for item in sublist]))

	def startValue(self):
		"""
		Start value
		"""
		return self._sequenceList[0].startInstant()._value

	def endValue(self):
		"""
		End value
		"""
		return self._sequenceList[-1].endInstant()._value

	def minValue(self):
		"""
		Minimum value
		"""
		return min(seq.minValue() for seq in self._sequenceList)

	def maxValue(self):
		"""
		Maximum value
		"""
		return max(seq.maxValue() for seq in self._sequenceList)

	def getTime(self):
		"""
		Period set on which the temporal value is defined
		"""
		return PeriodSet([seq.period() for seq in self._sequenceList])

	def period(self):
		"""
		Period on which the temporal value is defined ignoring the potential time gaps
		"""
		return Period(self.startTimestamp(), self.endTimestamp(),
					  self._sequenceList[0]._lower_inc, self._sequenceList[-1]._upper_inc)

	def numInstants(self):
		"""
		Number of distinct instants
		"""
		return len(self.instants())

	def startInstant(self):
		"""
		Start instant
		"""
		return self._sequenceList[0].startInstant()

	def endInstant(self):
		"""
		End instant
		"""
		return self._sequenceList[-1].endInstant()

	def instantN(self, n):
		"""
		N-th distinct instant
		"""
		# 1-based
		if 1 <= n <= len(self.instants()):
			return (self.instants())[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def instants(self):
		"""
		Instants
		"""
		instantList = []
		for sequence in self._sequenceList:
			for instant in sequence._instantList:
				instantList.append(instant)
		return instantList

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self.timestamps())

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._sequenceList[0].startInstant().getTimestamp()

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._sequenceList[-1].endInstant().getTimestamp()

	def timestampN(self, n):
		"""
		N-th timestamp
		"""
		# 1-based
		if 1 <= n <= len(self.timestamps()):
			return (self.timestamps())[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def timestamps(self):
		"""
		Timestamps
		"""
		timestampList = []
		for sequence in self._sequenceList:
			for instant in sequence._instantList:
				timestampList.append(instant.getTimestamp())
		# Remove duplicates
		timestampList = list(dict.fromkeys(timestampList))
		return timestampList

	def numSequences(self):
		"""
		Number of sequences
		"""
		return len(self._sequenceList)

	def startSequence(self):
		"""
		Start sequence
		"""
		return self._sequenceList[0]

	def endSequence(self):
		"""
		End sequence
		"""
		return self._sequenceList[-1]

	def sequenceN(self, n):
		"""
		N-th sequence
		"""
		# 1-based
		if 1 <= n <= len(self._sequenceList):
			return self._sequenceList[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def sequences(self):
		"""
		Sequences
		"""
		return self._sequenceList

	def shift(self, timedelta):
		"""
		Shift
		"""
		for seq in self._sequenceList:
			seq = seq.shift(timedelta)
		return self

	def intersectsTimestamp(self, timestamp):
		"""
		Intersects timestamp?
		"""
		return any(seq.intersectsTimestamp(timestamp) for seq in self._sequenceList)

	def intersectsTimestampset(self, timestampset):
		"""
		Intersects timestamp set?
		"""
		return any(seq.intersectsTimestamp(timestamp) for seq in self._sequenceList for timestamp in
				   timestampset._datetimeList)

	def intersectsPeriod(self, period):
		"""
		Intersects period?
		"""
		return any(seq.intersectsPeriod(period) for seq in self._sequenceList)

	def intersectsPeriodset(self, periodset):
		"""
		Intersects period set?
		"""
		return any(seq.intersectsPeriod(period) for seq in self._sequenceList for period in periodset._periodList)

	# Comparisons are missing
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._sequenceList == other._sequenceList and self._interp == other._interp:
				return True
		return False

	def __str__(self):
		interp_str = 'Interp=Stepwise;' if self._interp == 'Stepwise' and self.__class__.BaseClassDiscrete == False else ''
		seqList_str = "{{{}}}".format(
			', '.join('{}'.format(sequence.__str__().replace("'", "").replace("Interp=Stepwise;", ""))
					  for sequence in self._sequenceList))
		return f"'{interp_str}{seqList_str}'"

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._sequenceList!r}, {self._interp!r})')
