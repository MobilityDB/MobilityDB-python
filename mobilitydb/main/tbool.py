from parsec import *
from datetime import datetime
from dateutil.parser import parse
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS
from mobilitydb.temporal.temporal_parser import parse_temporalinst


class TBool(Temporal):
	"""
	Temporal booleans of any duration (abstract class)
	"""

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TBoolInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TBoolSeq(value)
		elif value[0] == '{':
			if value[1] == '[' or value[1] == '(':
				return TBoolS(value)
			else:
				return TBoolI(value)
		raise Exception("ERROR: Could not parse temporal boolean value")

	@staticmethod
	def write(value):
		if not isinstance(value, TBool):
			raise ValueError('TBool value must subclass TBool class')
		return value.__str__().strip("'")


class TBoolInst(TemporalInst, TBool):
	"""
	Temporal booleans of instant duration
	"""

	"""It is not possible to call super().__init__(value, time) since bool('False') == True
	and eval('False') == False. Furthermore eval('false') gives an error
	"""
	def __init__(self, value, time=None):
		TemporalInst.BaseClass = bool
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
		assert(isinstance(value, (str, bool)))
		assert(isinstance(time, (str, datetime)))
		if isinstance(value, str):
			if value.lower() == 'true' or value.lower() == 't':
				self._value = True
			elif value.lower() == 'false' or value.lower() == 'f':
				self._value = False
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
		else:
			self._value =  value
		self._time = parse(time) if isinstance(time, str) else time


class TBoolI(TemporalI, TBool):
	"""
	Temporal booleans of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = bool
		TemporalI.ComponentClass = TBoolInst
		super().__init__(*argv)


class TBoolSeq(TemporalSeq, TBool):
	"""
	Temporal booleans of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None, interp='Stepwise'):
		TemporalSeq.BaseClass = bool
		TemporalSeq.BaseClassDiscrete = True
		TemporalSeq.ComponentClass = TBoolInst
		self._interp = 'Stepwise'
		super().__init__(instantList, lower_inc, upper_inc)

	@classmethod
	def interpolation(self):
		return 'Stepwise'


class TBoolS(TemporalS, TBool):
	"""
	Temporal booleans of sequence set duration
	"""

	def __init__(self, sequenceList, interp='Stepwise'):
		TemporalS.BaseClass = bool
		TemporalS.BaseClassDiscrete = True
		TemporalS.ComponentClass = TBoolSeq
		self._interp = 'Stepwise'
		super().__init__(sequenceList)

	@classmethod
	def interpolation(self):
		return 'Stepwise'

