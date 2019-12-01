from MobilityDB.TemporalTypes import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


class TBool(Temporal):
	"""
	Temporal booleans of any duration (abstract class)
	"""
	Interpolation = 'stepwise'

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TBoolInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TBoolSeq(value)
		elif (value[0] == '{'):
			if value[1] == '[' or value[1] == '(':
				return TBoolS(value)
			else:
				return TBoolI(value)
		raise Exception("ERROR: Could not parse temporal float value")


class TBoolInst(TemporalInst, TBool):
	"""
	Temporal booleans of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = str
		super().__init__(value, time)


class TBoolI(TemporalI, TBool):
	"""
	Temporal booleans of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = str
		TemporalI.ComponentClass = TBoolInst
		super().__init__(*argv)


class TBoolSeq(TemporalSeq, TBool):
	"""
	Temporal booleans of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseClass = str
		TemporalSeq.ComponentClass = TBoolInst
		super().__init__(instantList, lower_inc, upper_inc)


class TBoolS(TemporalS, TBool):
	"""
	Temporal booleans of sequence set duration
	"""

	def __init__(self, *argv):
		TemporalS.BaseClass = str
		TemporalS.ComponentClass = TBoolSeq
		super().__init__(*argv)


