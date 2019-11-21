from MobilityDB.TimeTypes.period import PERIOD

class TEMPORALS:
	__slots__ = ['_sequenceList']
	Duration = 4

	def __init__(self, sequenceList=None):
		if isinstance(sequenceList, list):
			self._sequenceList = sequenceList.copy()

	def period(self):
		"""

		"""
		return PERIOD(self.startTimestamp(), self.endTimestamp(),
			self._sequenceList[0].lower_inc, self._sequenceList[-1].upper_inc)

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

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self.timestamps())

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._sequenceList[0].startTimestamp()

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._sequenceList[-1].endTimestamp()

	def timestampN(self, n):
		"""
		N-th distinct timestamp
		"""
		# 1-based
		if 0 < n <= len(self.timestamps()):
			return (self.timestamps())[n - 1]
		else:
			raise Exception("ERROR: there is no value at this index")

	def timestamps(self):
		"""
		Distinct timestamps
		"""
		timestampList = []
		for sequence in self._sequenceList:
			for instant in self.sequence:
				timestampList.append(instant.getTimestamp())
		# Remove duplicates
		timestampList = list(dict.fromkeys(timestampList))
		return timestampList

	def __str__(self):
		return "{}{{{}}}".format("", self.sequences())
