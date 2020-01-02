from datetime import datetime
from bdateutil.parser import parse
from MobilityDB.TemporalTypes import *
from postgis import Geometry, Point, MultiPoint, LineString, GeometryCollection, MultiLineString


# Add method to Point to make the class hashable
def __hash__(self):
	return hash(self.values())

setattr(Point, '__hash__', __hash__)


class TGeogPoint(Temporal):
	"""
	Temporal geographic points of any duration (abstract class)
	"""

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value.startswith('Interp=Stepwise;'):
			value1 = value.replace('Interp=Stepwise;', '')
			if value1[0] == '{':
				return TGeogPointS(value)
			else:
				return TGeogPointSeq(value)
		elif value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TGeogPointInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TGeogPointSeq(value)
		elif (value[0] == '{'):
			if value[1] == '[' or value[1] == '(':
				return TGeogPointS(value)
			else:
				return TGeogPointI(value)
		raise Exception("ERROR: Could not parse temporal float value")


class TGeogPointInst(TemporalInst, TGeogPoint):
	"""
	Temporal geographic points of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = Point
		# Constructor with a single argument of type string
		if time is None and isinstance(value, str):
			splits = value.split("@")
			if len(splits) == 2:
				if '(' in splits[0] and ')' in splits[0]:
					idx1 = splits[0].find('(')
					idx2 = splits[0].find(')')
					coords = (splits[0][idx1 + 1:idx2]).split(' ')
					self._value = type(self).BaseClass(coords)
				else:
					self._value = Geometry.from_ewkb(splits[0])
				self._time = parse(splits[1])
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
		# Constructor with two arguments of type string
		elif isinstance(value, str) and isinstance(time, str):
			if '(' in value and ')' in value:
				idx1 = value.find('(')
				idx2 = value.find(')')
				coords = (value[idx1 + 1:idx2]).split(' ')
				self._value = self.BaseClass(coords)
			else:
				self._value = Geometry.from_ewkb(value)
			self._time = parse(time)
		# Constructor with two arguments of type BaseClass and datetime
		elif isinstance(value, self.BaseClass) and isinstance(time, datetime):
			self._value = value
			self._time = time
		else:
			raise Exception("ERROR: Could not parse temporal instant value")

	def getValues(self):
		"""
		Distinct values
		"""
		return self._value


class TGeogPointI(TemporalI, TGeogPoint):
	"""
	Temporal geographic points of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = Point
		TemporalI.ComponentClass = TGeogPointInst
		super().__init__(*argv)

	def getValues(self):
		"""
		Distinct values
		"""
		values = super().getValues()
		return MultiPoint(values)


class TGeogPointSeq(TemporalSeq, TGeogPoint):
	"""
	Temporal geographic points of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None, interp=None):
		TemporalSeq.BaseClass = Point
		TemporalSeq.BaseClassDiscrete = False
		TemporalSeq.ComponentClass = TGeogPointInst
		super().__init__(instantList, lower_inc, upper_inc, interp)

	def interpolation(self):
		"""
		Interpolation
		"""
		return self._interp

	def getValues(self):
		"""
		Distinct values
		"""
		values = [inst._value for inst in self._instantList]
		result = values[0] if len(values) == 1 else LineString(values)
		return result


class TGeogPointS(TemporalS, TGeogPoint):
	"""
	Temporal geographic points of sequence set duration
	"""

	def __init__(self, sequenceList, interp=None):
		TemporalS.BaseClass = Point
		TemporalS.BaseClassDiscrete = False
		TemporalS.ComponentClass = TGeogPointSeq
		super().__init__(sequenceList, interp)

	def interpolation(self):
		"""
		Interpolation
		"""
		return self._interp

	def getValues(self):
		"""
		Distinct values
		"""
		values = [seq.getValues() for seq in self._sequenceList]
		points = [geo for geo in values if isinstance(geo, Point)]
		lines = [geo for geo in values if isinstance(geo, LineString)]
		if len(points) != 0 and len(points) != 0:
			return GeometryCollection(points + lines)
		if len(points) != 0 and len(points) == 0:
			return MultiPoint(points)
		if len(points) == 0 and len(points) != 0:
			return MultiLineString(lines)

