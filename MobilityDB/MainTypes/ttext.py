from datetime import datetime
from bdateutil.parser import parse
from MobilityDB.TemporalTypes.temporal_parser import parse_temporalinst
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
		# Constructor with a single argument of type string
		if isinstance(value, str) and time is None:
			couple = parse_temporalinst(value, 0)
			# Remove double quotes if present
			if couple[2][0][0] == '"' and couple[2][0][0][-1] == '"':
				couple[2][0] = couple[2][0][1:-1]
			self._value = type(self).BaseClass(couple[2][0])
			self._time = parse(couple[2][1])
		# Constructor with two arguments of type string
		elif isinstance(value, str) and isinstance(time, str):
			if value[0] == '"' and value[-1] == '"':
				value = value[1:-1]
			self._value = self.BaseClass(value)
			self._time = parse(time)
		# Constructor with two arguments of type BaseClass and datetime
		elif isinstance(value, self.BaseClass) and isinstance(time, datetime):
			self._value = value
			self._time = time
		# Constructor with one argument of type list
		elif isinstance(value, tuple):
			self._value = self.BaseClass(value[0])
			self._time = parse(value[1])
		else:
			raise Exception("ERROR: Could not parse temporal instant value")


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

	def __init__(self, instantList, lower_inc=None, upper_inc=None, interp='Stepwise'):
		TemporalSeq.BaseClass = str
		TemporalS.BaseClassDiscrete = True
		TemporalSeq.ComponentClass = TTextInst
		super().__init__(instantList, lower_inc, upper_inc, interp)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


class TTextS(TemporalS, TText):
	"""
	Temporal texts of sequence set duration
	"""

	def __init__(self, sequenceList, interp='Stepwise'):
		TemporalS.BaseClass = str
		TemporalS.BaseClassDiscrete = True
		TemporalS.ComponentClass = TTextSeq
		super().__init__(sequenceList, interp)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


