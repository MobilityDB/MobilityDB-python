from datetime import datetime
from bdateutil.parser import parse
from .temporal import TEMPORAL
from MobilityDB.TimeTypes.period import PERIOD

class TEMPORALINST(TEMPORAL):
	__slots__ = ['_value', '_time']
	Duration = 1

	def __init__(self, value, time=None):
		# Constructor with a single argument of type string
		if time is None and isinstance(value, str):
			splits = value.split("@")
			if len(splits == 2):
				self._value = parse(splits[0])
				self._time = parse(splits[1])
			else:
				raise Exception("ERROR: Could not temporal instant value")
			print(self._value)
			print(self._time)
		# Constructor with two arguments of type string and optional arguments for the bounds
		elif isinstance(value, str) and isinstance(time, str):
			self._value = parse(value)
			self._time = parse(time)
		else:
			raise Exception("ERROR: Could not temporal instant value")

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
		return self.SubClass._value

	def getTimestamp(self):
		"""
		Timestamp
		"""
		return self.SubClass._time

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
		return self.SubClass._time

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self.SubClass._time

	def timestampN(self, n):
		"""
		N-th distinct timestamp
		"""
		if n == 1:
			return self.SubClass._time
		else:
			raise Exception("ERROR: Out of range")

	def timestamps(self):
		"""
		Timestamps
		"""
		return [self.SubClass._time]

	def __str__(self):
		#return self.__class__.__bases__[0].__name__ + " '" + self.SubClass.__str__() + "'"
		return "'" + self.SubClass._time.__str__() + '@'+ self.SubClass._time.__str__() + "'"
