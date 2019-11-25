from abc import abstractmethod
from MobilityDB.TimeTypes import *

class TEMPORAL:
	"""
	...
	General example:
		>>> var1 = TINTINST('10@2019-09-10')
		>>> var2 = TGEOMPOINTINST('SRID=4326;Point(1 1)@2019-09-10')
	"""
	BaseValueClass = None
	SubClass = None

	@classmethod
	def duration(cls):
		"""
		Duration
		"""
		pass

	def timespan(self):
		"""
		Interval
		"""
		return self.endTimestamp() - self.startTimestamp()

	@abstractmethod
	def getValues(self):
		"""
		Values
		"""
		pass

	@abstractmethod
	def getTime(self):
		"""
		Time
		"""
		pass

	@abstractmethod
	def timespan(self):
		"""
		Timespan
		"""
		pass

	@abstractmethod
	def period(self):
		"""
		Period on which the temporal value is defined ignoring potential time gaps
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
	def numTimestamp(self):
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

	# Comparisons are missing
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return True

	def __str__(self):
		if len(self.__class__.__bases__) == 2:
			return self.__class__.__bases__[0].__name__ + " '" + self.SubClass.__str__() + "'"
		else:
			return self.__class__.__name__ + " '" + self.SubClass.__str__() + "'"
