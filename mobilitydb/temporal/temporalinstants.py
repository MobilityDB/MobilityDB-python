from .temporal import Temporal


class TemporalInstants(Temporal):
	__slots__ = ['_instantList']

	def getValues(self):
		"""
		Distinct values
		"""
		return list(dict.fromkeys([inst._value for inst in self._instantList]))

	def startValue(self):
		"""
		Start value
		"""
		return self._instantList[0]._value

	def endValue(self):
		"""
		End value
		"""
		return self._instantList[-1]._value

	def minValue(self):
		"""
		Minimum value
		"""
		return min(inst._value for inst in self._instantList)

	def maxValue(self):
		"""
		Maximum value
		"""
		return max(inst._value for inst in self._instantList)

	def numInstants(self):
		"""
		Number of distinct instants
		"""
		return len(self._instantList)

	def startInstant(self):
		"""
		Start instant
		"""
		return self._instantList[0]

	def endInstant(self):
		"""
		End instant
		"""
		return self._instantList[-1]

	def instantN(self, n):
		"""
		N-th distinct instant
		"""
		# 1-based
		if 1 <= n <= len(self._instantList):
			return self._instantList[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def instants(self):
		"""
		Instants
		"""
		return self._instantList

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self._instantList)

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._instantList[0]._time

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._instantList[-1]._time

	def timestampN(self, n):
		"""
		N-th timestamp
		"""
		# 1-based
		if 1 <= n <= len(self._instantList):
			return self._instantList[n - 1]._time
		else:
			raise Exception("ERROR: Out of range")

	def timestamps(self):
		"""
		Timestamps
		"""
		return [instant._time for instant in self._instantList]

	def shift(self, timedelta):
		"""
		Shift
		"""
		for inst in self._instantList:
			inst._time += timedelta
		return self

	def __str__(self):
		return "{}".format(', '.join('{}'.format(instant.__str__().replace("'", ""))
			for instant in self._instantList))
