from abc import abstractmethod
from MobilityDB.TimeTypes import *


class Temporal:
	"""
	Abstract class for temporal types of any duration
	"""
	BaseClass = None
	ComponentClass = None

	@classmethod
	def duration(cls):
		"""
		Duration
		"""
		pass

	@abstractmethod
	def getValues(self):
		"""
		Values
		"""
		pass

	@abstractmethod
	def startValue(self):
		"""
		Start value
		"""
		pass

	@abstractmethod
	def endValue(self):
		"""
		Start value
		"""
		pass

	@abstractmethod
	def minValue(self):
		"""
		Minimum value
		"""
		pass

	@abstractmethod
	def maxValue(self):
		"""
		Maximum value
		"""
		pass

	@abstractmethod
	def getTime(self):
		"""
		Time
		"""
		pass

	def timespan(self):
		"""
		Interval
		"""
		return self.endTimestamp() - self.startTimestamp()

	@abstractmethod
	def period(self):
		"""
		Period on which the temporal value is defined ignoring potential time gaps
		"""
		pass

	@abstractmethod
	def numInstants(self):
		"""
		Number of distinct instants
		"""
		pass

	@abstractmethod
	def startInstant(self):
		"""
		 Start instant
		"""
		pass

	@abstractmethod
	def endInstant(self):
		"""
		End instant
		"""
		pass

	@abstractmethod
	def instantN(self, n):
		"""
		N-th instant
		"""
		pass

	@abstractmethod
	def instants(self):
		"""
		Instants
		"""
		pass

	@abstractmethod
	def numTimestamps(self):
		"""
		Number of distinct instants
		"""
		pass

	@abstractmethod
	def startTimestamp(self):
		"""
		 Start instant
		"""
		pass

	@abstractmethod
	def endTimestamp(self):
		"""
		End instant
		"""
		pass

	@abstractmethod
	def timestampN(self, n):
		"""
		N-th timestamp
		"""
		pass

	@abstractmethod
	def timestamps(self):
		"""
		Timestamps
		"""
		pass

	@abstractmethod
	def shift(self, timedelta):
		"""
		Shift
		"""
		pass

	@abstractmethod
	def intersectsTimestamp(self, datetime):
		"""
		Intersects timestamp
		"""
		pass

	@abstractmethod
	def intersectsTimestampset(self, timestampset):
		"""
		Intersects timestamp set
		"""
		pass

	@abstractmethod
	def intersectsPeriod(self, period):
		"""
		Intersects period
		"""
		pass

	@abstractmethod
	def intersectsPeriodset(self, periodset):
		"""
		Intersects period set
		"""
		pass

	# Comparisons are missing
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return True

	def __str__(self):
		"""
		String representation
		"""
		pass
