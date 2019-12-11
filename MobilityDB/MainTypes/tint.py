from spans.types import Range
from MobilityDB.TemporalTypes import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


class intrange(Range):
	__slots__ = ()
	type = int

class TInt(Temporal):
	"""
	Temporal integers of any duration (abstract class)
	"""

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TIntInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TIntSeq(value)
		elif value[0] == '{':
			if value[1] == '[' or value[1] == '(':
				return TIntS(value)
			else:
				return TIntI(value)
		raise Exception("ERROR: Could not parse temporal integer value")

	def valueRange(self):
		"""
		Distinct values
		"""
		return intrange(self.minValue(), self.maxValue(), True, True)


class TIntInst(TemporalInst, TInt):
	"""
	Temporal integers of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = int
		super().__init__(value, time)


class TIntI(TemporalI, TInt):
	"""
	Temporal integers of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = int
		TemporalI.ComponentClass = TIntInst
		super().__init__(*argv)


class TIntSeq(TemporalSeq, TInt):
	"""
	Temporal integers of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseClass = int
		TemporalSeq.ComponentClass = TIntInst
		super().__init__(instantList, lower_inc, upper_inc)

	@classmethod
	def interpolation(self):
		return 'Stepwise'



class TIntS(TemporalS, TInt):
	"""
	Temporal integers of sequence set duration
	"""

	def __init__(self, *argv):
		TemporalS.BaseClass = int
		TemporalS.ComponentClass = TIntSeq
		super().__init__(*argv)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


