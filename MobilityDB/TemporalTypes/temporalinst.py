from datetime import datetime
from bdateutil.parser import parse
from .temporal import TEMPORAL
from MobilityDB.TimeTypes.period import PERIOD
from MobilityDB.TimeTypes.periodset import PERIODSET

class TEMPORALINST(TEMPORAL):
	__slots__ = ['_value', '_time']

	def __init__(self, value, time=None):
		# Constructor with a single argument of type string
		if time is None and isinstance(value, str):
			splits = value.split("@")
			if len(splits) == 2:
				self._value = type(self).BaseValueClass(splits[0])
				self._time = parse(splits[1])
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
		# Constructor with two arguments of type string
		elif isinstance(value, str) and isinstance(time, str):
			self._value = self.BaseValueClass(value)
			self._time = parse(time)
		# Constructor with two arguments of type BaseValueClass and datetime
		elif isinstance(value, self.BaseValueClass) and isinstance(time, datetime):
			self._value = value
			self._time = time
		else:
			raise Exception("ERROR: Could not parse temporal instant value")

	@classmethod
	def duration(cls):
		return "Instant"

	def getValue(self):
		"""
		Retrieve the base value [getValue():  base]
			>>> var1.getValue()
				<Point: Geometry(Point, 4326)>
			>>> var2.getValue()
				10
		"""
		return self._value

	def getValues(self):
		"""
		Retrieve the base value [getValue():  base]
			>>> var1.getValue()
				<Point: Geometry(Point, 4326)>
			>>> var2.getValue()
				10
		"""
		return [self._value]

	def startValue(self):
		"""
		Start value
		"""
		return self._value

	def endValue(self):
		"""
		Start value
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
		Timestamp
		"""
		return PERIODSET([PERIOD(self._time, self._time, True, True)])

	def period(self):
		"""
		Period on which the temporal value is defined
		"""
		return PERIOD(self.getTimestamp(), self.getTimestamp(), True, True)

	def numInstants(self):
		"""
		Number of instants
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
		N-th instant
		"""
		if n == 1:
			return self
		else:
			raise Exception("ERROR: Out of range")

	def instants(self):
		"""
		Instants
		"""
		return [self]

	def numTimestamps(self):
		"""
		Number of distinct instants
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
		Intersects timestamp
		"""
		return self._time == timestamp

	def intersectsTimestampset(self, timestampset):
		"""
		Intersects timestamp set
		"""
		return any(self._time == timestamp for timestamp in timestampset._datetimeList)

	def intersectsPeriod(self, period):
		"""
		Intersects period
		"""
		return period.contains_timestamp(self._time)

	def intersectsPeriodset(self, periodset):
		"""
		Intersects period set
		"""
		return any(period.contains_timestamp(self._time) for period in periodset._periodList)

	def __str__(self):
		#return self.__class__.__bases__[0].__name__ + " '" + self.__str__() + "'"
		return "'" + self._value.__str__() + '@' + self._time.__str__() + "'"
