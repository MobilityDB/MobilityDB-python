from MobilityDB.TemporalTypes import *
from spans.types import Range

class intrange(Range):
	__slots__ = ()
	type = int


class TINT(TEMPORAL):
	BaseValueClass = int

	def valueRange(self):
		"""
		Distinct values
		"""
		return intrange(self.minValue(), self.maxValue(), True, True)

class TINTINST(TEMPORALINST, TINT):

	def __init__(self, value, time=None):
		super().__init__(value, time)
		TEMPORALINST.BaseValueClass = int

class TINTI(TEMPORALI, TINT):

	def __init__(self,  *argv):
		super().__init__(*argv)
		TEMPORALI.BaseValueClass = int

class TINTSEQ(TEMPORALSEQ, TINT):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		super().__init__(instantList, lower_inc, upper_inc)
		TEMPORALSEQ.BaseValueClass = int

	def getValues(self):
		"""
		Distinct values
		"""
		return intrange(self.minValue(), self.maxValue())

class TINTS(TEMPORALS, TINT):

	def __init__(self, *argv):
		super().__init__(*argv)
		TEMPORALS.BaseValueClass = int

	def getValues(self):
		"""
		Distinct values
		"""
		return intrange(self.minValue(), self.maxValue())

