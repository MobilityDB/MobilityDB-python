from MobilityDB.TemporalTypes import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


class TText(Temporal):
	"""
	Temporal texts of any duration (abstract class)
	"""

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TTextInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TTextSeq(value)
		elif value[0] == '{':
			if value[1] == '[' or value[1] == '(':
				return TTextS(value)
			else:
				return TTextI(value)
		raise Exception("ERROR: Could not parse temporal text value")


class TTextInst(TemporalInst, TText):
	"""
	Temporal texts of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = str
		super().__init__(value, time)


class TTextI(TemporalI, TText):
	"""
	Temporal texts of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = str
		TemporalI.ComponentClass = TTextInst
		super().__init__(*argv)


class TTextSeq(TemporalSeq, TText):
	"""
	Temporal texts of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseClass = str
		TemporalSeq.ComponentClass = TTextInst
		super().__init__(instantList, lower_inc, upper_inc)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


class TTextS(TemporalS, TText):
	"""
	Temporal texts of sequence set duration
	"""

	def __init__(self, *argv):
		TemporalS.BaseClass = str
		TemporalS.ComponentClass = TTextSeq
		super().__init__(*argv)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


