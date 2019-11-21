from MobilityDB.TimeTypes import *


class TEMPORAL:
	"""
	...
	General example:
		>>> var1 = TGEOMPOINTINST('SRID=4326;Point(1 1)@2019-09-10')
		>>> var2 = TINTINST('10@2019-09-10')
	"""
	BaseValueClass = None
	SubClass = None

	# Accessor functions
	def getValues(self):
		"""
		Values
		"""
		if self.SubClass.Duration == 1:
			return self.SubClass.value
		elif self.SubClass.Duration == 2:
			return [inst.value for inst in self.SubClass.value]
		elif self.SubClass.Duration == 3:
			return self.SubClass.getDistinctValues(self.BaseValueClass)

	@abstractproperty
	def period(self):
		"""
		Period on which the temporal value is defined ignoring potential time gaps
		"""
		pass

	def startInstant(self):
		"""
		 Start instant
		"""
		if self.SubClass.Duration == 1:
			return self.SubClass
		elif self.SubClass.Duration in [2, 3]:
			return self.__class__(self.SubClass.startInstant())
		else:
			raise Exception("ERROR:  Could not parse temporal value")

	def endInstant(self):
		"""
		End instant
		"""
		if self.SubClass.Duration == 1:
			return self.SubClass
		elif self.SubClass.Duration in [2, 3]:
			return self.SubClass.endInstant()
		else:
		raise Exception("ERROR:  Could not parse temporal value")


	def startValue(self):
		"""

		"""
		if self.SubClass.Duration == 1:
			return self.SubClass.value
		elif self.SubClass.Duration in [2, 3]:
			return self.SubClass.startInstant().value

	def endValue(self):
		"""

		"""
		if self.SubClass.Duration == 1:
			return self.SubClass.value
		elif self.SubClass.Duration in [2, 3]:
			return self.SubClass.endInstant().value

	def duration(self):
		"""

		"""
		if self.SubClass.Duration == 1:
			return "Instant"
		elif self.SubClass.Duration == 2:
			return "InstantSet"
		elif self.SubClass.Duration == 3:
			return "Sequence"

	def instantN(self, n):
		"""

		"""
		if self.SubClass.Duration == 1 and n == 1:
			return self.SubClass
		elif self.SubClass.Duration in [2, 3] and 0 < n < self.SubClass.numInstants():
			return self.SubClass.value[n - 1]
		else:
			raise Exception("ERROR: there is no value at this index")

	def sequenceN(self, n):
		"""

		"""
		if 0 <= n < self.SubClass.numSequences():
			return self.SubClass.sequences[n]
		raise Exception("ERROR: out of range")


	def instants(self):
		"""

		"""
		return self.SubClass.getInstants()


	# Comparisons are missing
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return True

	def __str__(self):
		if len(self.__class__.__bases__) == 2:
			return self.__class__.__bases__[0].__name__ + " '" + self.SubClass.__str__() + "'"
		else:
			return self.__class__.__name__ + " '" + self.SubClass.__str__() + "'"
