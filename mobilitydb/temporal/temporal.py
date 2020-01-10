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
	"""

	BaseClass = None
	"""
	Class of the base type, e.g., float for TFloat
	"""

	BaseClassDiscrete = None
	"""
	Boolean that determines wheter the base type is discrete, e.g., True for int and False for float
	"""

	ComponentClass = None
	"""
	Class of the class of the components, e.g., 
	(1) TFloatInst for both TFloatI and TFloatSeq
	(2) TFloatSeq for TFloatS.
	"""

	@property
	@classmethod
	def duration(cls):
		"""
		Duration
		"""
		pass

	@property
	@abstractmethod
	def getValues(self):
		"""
		Values
		"""
		pass

	@property
	@abstractmethod
	def startValue(self):
		"""
		Start value
		"""
		pass

	@property
	@abstractmethod
	def endValue(self):
		"""
		End value
		"""
		pass

	@property
	@abstractmethod
	def minValue(self):
		"""
		Minimum value
		"""
		pass

	@property
	@abstractmethod
	def maxValue(self):
		"""
		Maximum value
		"""
		pass

	@property
	@abstractmethod
	def getTime(self):
		"""
		Period set on which the temporal value is defined
		"""
		pass

	@property
	def timespan(self):
		"""
		Interval
		"""
		return self.endTimestamp - self.startTimestamp

	@property
	@abstractmethod
	def period(self):
		"""
		Period on which the temporal value is defined ignoring potential time gaps
		"""
		pass

	@property
	@abstractmethod
	def numInstants(self):
		"""
		Number of distinct instants
		"""
		pass

	@property
	@abstractmethod
	def startInstant(self):
		"""
		 Start instant
		"""
		pass

	@property
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

	@property
	@abstractmethod
	def instants(self):
		"""
		Instants
		"""
		pass

	@property
	@abstractmethod
	def numTimestamps(self):
		"""
		Number of distinct instants
		"""
		pass

	@property
	@abstractmethod
	def startTimestamp(self):
		"""
		 Start instant
		"""
		pass

	@property
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

	@property
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
