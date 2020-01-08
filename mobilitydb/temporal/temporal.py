from abc import abstractmethod
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class Temporal:
	"""
	Abstract class for temporal types of any duration
	The class variables are as follows:
	* BaseClass: class of the base type, e.g., float
	* BaseClassDiscrete: whether the base type is discrete, e.g., False for float
	* Component Class: class of the components, e.g., TFloatInst for
	  both TFloatI and TFloatSeq or TFloatSeq for TFloatS.
	"""
	BaseClass = None
	BaseClassDiscrete = None
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
		Period set on which the temporal value is defined
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

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

	# Comparisons are missing
	def __eq__(self, other):
		"""
		Equality
		"""
		pass

	def __str__(self):
		"""
		String
		"""
		pass

	def __repr__(self):
		"""
		Representation
		"""
		pass
