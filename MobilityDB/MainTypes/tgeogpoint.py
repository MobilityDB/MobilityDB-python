from datetime import datetime
from bdateutil.parser import parse
from MobilityDB.TemporalTypes import *
from postgis import Point, MultiPoint, LineString, GeometryCollection, MultiLineString

# Add method to Point to make the class hashable
def __hash__(self):
	return hash(self.values())

setattr(Point, '__hash__', __hash__)


class TGeogPoint(Temporal):
	"""
	Temporal geographic points of any duration (abstract class)
	"""
	BaseValueClass = Point
	ComponentValueClass = None

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		print("value =", value)
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
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
		TemporalInst.BaseValueClass = Point
		#super().__init__(value, time)
		# Constructor with a single argument of type string
		if time is None and isinstance(value, str):
			splits = value.split("@")
			if len(splits) == 2:
				idx1 = splits[0].find('(')
				idx2 = splits[0].find(')')
				coords = (splits[0][idx1 + 1:idx2]).split(' ')
				self._value = type(self).BaseValueClass(coords)
				self._time = parse(splits[1])
			else:
				raise Exception("ERROR: Could not parse temporal instant value")
		# Constructor with two arguments of type string
		elif isinstance(value, str) and isinstance(time, str):
			idx1 = value.find('(')
			idx2 = value.find(')')
			coords = (value[idx1 + 1:idx2]).split(' ')
			self._value = self.BaseValueClass(coords)
			self._time = parse(time)
		# Constructor with two arguments of type BaseValueClass and datetime
		elif isinstance(value, self.BaseValueClass) and isinstance(time, datetime):
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
		TemporalI.BaseValueClass = Point
		TemporalI.ComponentValueClass = TGeogPointInst
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

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseValueClass = Point
		TemporalSeq.ComponentValueClass = TGeogPointInst
		super().__init__(instantList, lower_inc, upper_inc)

	def getValues(self):
		"""
		Distinct values
		"""
		values = super().getValues()
		if len(values) == 1:
			result = values[0]
		else:
			result = LineString(values)
		return result


class TGeogPointS(TemporalS, TGeogPoint):
	"""
	Temporal geographic points of sequence set duration
	"""

	def __init__(self, *argv):
		TemporalS.BaseValueClass = Point
		TemporalS.ComponentValueClass = TGeogPointSeq
		super().__init__(*argv)

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

