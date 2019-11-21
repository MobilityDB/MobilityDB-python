from MobilityDB.TimeTypes.period import PERIOD


class TEMPORALS:
	__slots__ = ['_sequenceList']
	Duration = 4

	def __init__(self, sequenceList=None):
		if isinstance(sequenceList, list):
			self._sequenceList = sequenceList.copy()

	@classmethod
	def duration(cls):
		return "SequenceSet"

	def period(self):
		"""
		Period on which the temporal value is defined ignoring the potential time gaps
		"""
		return PERIOD(self.startTimestamp(), self.endTimestamp(),
			self._sequenceList[0].lower_inc, self._sequenceList[-1].upper_inc)

	def startValue(self):
		"""
		Start value
		"""
		return self._sequenceList[0].startInstant()._value

	def endValue(self):
		"""
		Start value
		"""
		return self._sequenceList[len(self._sequenceList) - 1].startInstant()._value

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
		return self._sequenceList[len(self._sequenceList) - 1].endInstant()

	def instantN(self, n):
		"""
		N-th instant
		"""
		# 1-based
		if 0 <= n < len(self.instants()):
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
		# Remove duplicates
		instantList = list(dict.fromkeys(instantList))
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
		return self._sequenceList[len(self._sequenceList) - 1].endInstant().getTimestamp()

	def timestampN(self, n):
		"""
		N-th timestamp
		"""
		# 1-based
		if 0 <= n < len(self.timestamps()):
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
		return self._sequenceList[len(self._sequenceList) - 1]

	def sequenceN(self, n):
		"""
		N-th sequence
		"""
		# 1-based
		if 0 <= n < len(self._sequenceList):
			return self._sequenceList[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def sequences(self):
		"""
		Sequences
		"""
		return self._sequenceList

	def __str__(self):
		return "{{{}}}".format(', '.join('{}'.format(sequence.__str__().replace("'", ""))
			for sequence in self._sequenceList))
