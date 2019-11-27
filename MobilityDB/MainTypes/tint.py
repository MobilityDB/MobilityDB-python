from MobilityDB.TemporalTypes import *
from spans.types import Range


class intrange(Range):
	__slots__ = ()
	type = int

class TINT(TEMPORAL):
	BaseValueClass = int
	ComponentValueClass = None

	def valueRange(self):
		"""
		Distinct values
		"""
		return intrange(self.minValue(), self.maxValue(), True, True)

class TINTINST(TEMPORALINST, TINT):

	def __init__(self, value, time=None):
		TEMPORALINST.BaseValueClass = int
		super().__init__(value, time)

class TINTI(TEMPORALI, TINT):

	def __init__(self,  *argv):
		TEMPORALI.BaseValueClass = int
		TEMPORALI.ComponentValueClass = TINTINST
		super().__init__(*argv)

class TINTSEQ(TEMPORALSEQ, TINT):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TEMPORALSEQ.BaseValueClass = int
		TEMPORALSEQ.ComponentValueClass = TINTINST
		super().__init__(instantList, lower_inc, upper_inc)

class TINTS(TEMPORALS, TINT):

	def __init__(self, *argv):
		TEMPORALS.BaseValueClass = int
		TEMPORALS.ComponentValueClass = TINTSEQ
		super().__init__(*argv)


