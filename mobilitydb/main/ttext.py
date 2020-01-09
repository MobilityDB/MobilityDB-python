from datetime import datetime
from dateutil.parser import parse
from mobilitydb.temporal.temporal_parser import parse_temporalinst
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


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

	@staticmethod
	def write(value):
		if not isinstance(value, TText):
			raise ValueError('TText value must subclass TText class')
		return value.__str__().strip("'")


class TTextInst(TemporalInst, TText):
	"""
	Temporal texts of instant duration
	"""

	"""It is not possible to call super().__init__(value, time) since it is necessary
	to strip the eventual double quotes enclosing the value
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = str
		if(time is None):
			# Constructor with a single argument of type string
			if (isinstance(value, str)):
				couple = parse_temporalinst(value, 0)
				value = couple[2][0]
				time = couple[2][1]
			# Constructor with a single argument of type tuple or list
			elif (isinstance(value, (tuple, list))):
				value, time = value
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
		# Now both value and time are not None
		assert(isinstance(value, str))
		assert(isinstance(time, (str, datetime)))
		# Remove double quotes if present
		if value[0] == '"' and value[-1] == '"':
			value = value[1:-1]
		self._value = value
		self._time = parse(time) if isinstance(time, str) else time


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


