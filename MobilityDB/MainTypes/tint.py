from MobilityDB.TemporalTypes import *
from spans.types import Range


class intrange(Range):
	__slots__ = ()
	type = int

class TInt(Temporal):
	BaseValueClass = int
	ComponentValueClass = None

	def valueRange(self):
		"""
		Distinct values
		"""
		return intrange(self.minValue(), self.maxValue(), True, True)

class TIntInst(TemporalInst, TInt):

	def __init__(self, value, time=None):
		TemporalInst.BaseValueClass = int
		super().__init__(value, time)

class TIntI(TemporalI, TInt):

	def __init__(self,  *argv):
		TemporalI.BaseValueClass = int
		TemporalI.ComponentValueClass = TIntInst
		super().__init__(*argv)

class TIntSeq(TemporalSeq, TInt):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseValueClass = int
		TemporalSeq.ComponentValueClass = TIntInst
		super().__init__(instantList, lower_inc, upper_inc)

class TIntS(TemporalS, TInt):

	def __init__(self, *argv):
		TemporalS.BaseValueClass = int
		TemporalS.ComponentValueClass = TIntSeq
		super().__init__(*argv)


