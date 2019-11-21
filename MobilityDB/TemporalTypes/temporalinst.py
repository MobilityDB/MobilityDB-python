from .temporal import TEMPORAL


class TEMPORALINST(TEMPORAL):
	__slots__ = ['_value', '_time']
	Duration = 1

	def __init__(self, value=None, time=None):
		self._value = value
		self._time = time

	def getValue(self):
		"""
		Retrieve the base value [getValue():  base]
			>>> var1.getValue()
				<Point: Geometry(Point, 4326)>
			>>> var2.getValue()
				10
		"""
		return self._value

	def getTimestamp(self):
		"""

		"""
		return self._time

	def period(self):
		"""

		"""
		return PERIOD(self._time, self._time, True, True)

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

	def startTimestamp(self):
		"""
		Start instant
		"""
		return self._time

	def endTimestamp(self):
		"""
		End instant
		"""
		return self._time

	def timestampN(self, n):
		"""
		N-th instant
		"""
		if n == 1:
			return self._time
		else:
			raise Exception("ERROR: Out of range")

	def timestamps(self):
		"""
		Instants
		"""
		return [self._time]

	def __str__(self):
		if self.SubClass.__class__ == TEMPORALINST:
			return self.__class__.__bases__[0].__name__ + " '" + self.SubClass.__str__() + "'"
		else:
			return "{}{}".format(self._value.__str__() + "@", self._time.__str__())
