from spans.types import intrange
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


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

	@staticmethod
	def write(value):
		if not isinstance(value, TInt):
			raise ValueError('TInt value must subclass TInt class')
		return value.__str__().strip("'")

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
		TemporalSeq.BaseClassDiscrete = True
		TemporalSeq.ComponentClass = TIntInst
		super().__init__(instantList, lower_inc, upper_inc)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


class TIntS(TemporalS, TInt):
	"""
	Temporal integers of sequence set duration
	"""

	def __init__(self, sequenceList):
		TemporalS.BaseClass = int
		TemporalS.BaseClassDiscrete = True
		TemporalS.ComponentClass = TIntSeq
		super().__init__(sequenceList)

	@classmethod
	def interpolation(self):
		return 'Stepwise'

