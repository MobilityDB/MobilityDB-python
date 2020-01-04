from parsec import *
from datetime import datetime
from bdateutil.parser import parse
from .temporal import Temporal
from MobilityDB.TimeTypes.period import Period
from MobilityDB.TimeTypes.periodset import PeriodSet
from MobilityDB.TemporalTypes.temporal_parser import parse_temporalinst


class TemporalInst(Temporal):
	"""
	Abstract class for temporal types of instant duration
	"""
	__slots__ = ['_value', '_time']

	def __init__(self, value, time=None):
		# Constructor with a single argument of type string
		if isinstance(value, str) and time is None:
			couple = parse_temporalinst(value, 0)
			self._value = type(self).BaseClass(couple[2][0])
			self._time = parse(couple[2][1])
		# Constructor with two arguments
		elif value is not None and time is not None:
			if isinstance(value, str):
				self._value = type(self).BaseClass(value)
			elif isinstance(value, self.BaseClass):
				self._value = value
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
			if isinstance(time, str):
				self._time = parse(time)
			elif isinstance(time, datetime):
				self._time = time
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
		# Constructor with one argument of type list
		elif isinstance(value, tuple):
			self._value = self.BaseClass(value[0])
			self._time = parse(value[1])
		else:
			raise Exception("ERROR: Could not parse temporal instant value")

	@classmethod
	def duration(cls):
		return "Instant"

	def getValue(self):
		"""
		Value
		"""
		return self._value

	def getValues(self):
		"""
		Distinct values
		"""
		return [self._value]

	def startValue(self):
		"""
		Start value
		"""
		return self._value

	def endValue(self):
		"""
		End value
		"""
		return self._value

	def minValue(self):
		"""
		Minimum value
		"""
		return self._value

	def maxValue(self):
		"""
		Maximum value
		"""
		return self._value

	def getTimestamp(self):
		"""
		Timestamp
		"""
		return self._time

	def getTime(self):
		"""
		Period set on which the temporal value is defined
		"""
		return PeriodSet([Period(self._time, self._time, True, True)])

	def period(self):
		"""
		Period on which the temporal value is defined ignoring the potential time gaps
		"""
		return Period(self._time, self._time, True, True)

	def numInstants(self):
		"""
		Number of distinct instants
		"""
		return 1

	def startInstant(self):
		"""
		Start instant
		"""
		return self

	def endInstant(self):
		"""
		End instant
		"""
		return self

	def instantN(self, n):
		"""
		N-th distinct instant
		"""
		if n == 1:
			return self
		else:
			raise Exception("ERROR: Out of range")

	def instants(self):
		"""
		Distinct instants
		"""
		return [self]

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return 1

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._time

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._time

	def timestampN(self, n):
		"""
		N-th distinct timestamp
		"""
		if n == 1:
			return self._time
		else:
			raise Exception("ERROR: Out of range")

	def timestamps(self):
		"""
		Timestamps
		"""
		return [self._time]

	def shift(self, timedelta):
		"""
		Shift
		"""
		self._time += timedelta
		return self

	def intersectsTimestamp(self, timestamp):
		"""
		Intersects the timestamp?
		"""
		return self._time == timestamp

	def intersectsTimestampset(self, timestampset):
		"""
		Intersects the timestamp set?
		"""
		return any(self._time == timestamp for timestamp in timestampset._datetimeList)

	def intersectsPeriod(self, period):
		"""
		Intersects the period?
		"""
		return period.contains_timestamp(self._time)

	def intersectsPeriodset(self, periodset):
		"""
		Intersects the period set?
		"""
		return any(period.contains_timestamp(self._time) for period in periodset._periodList)

	# Comparisons are missing
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._value == other._value and self._time == other._time:
				return True
		return False

	def __str__(self):
		return (f"'{self._value!s}@{self._time!s}'")

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._value!r}, {self._time!r})')

