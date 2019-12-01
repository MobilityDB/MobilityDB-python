import re
from datetime import datetime
from bdateutil.parser import parse
from postgis import Geometry, Point, MultiPoint, LineString, GeometryCollection, MultiLineString
from MobilityDB.TemporalTypes import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


# Add method to Point to make the class hashable
def __hash__(self):
	return hash(self.values())

setattr(Point, '__hash__', __hash__)


class TGeomPoint(Temporal):
	"""
	Temporal geometric points of any duration (abstract class)
	"""
	Interpolation = 'linear'

	def has_z(self):
		"""
		Returns True if the temporal point has Z dimension
		"""
		return self.startValue().z is not None

	def srid(self):
		"""
		Returns True if the temporal point has Z dimension
		"""
		result = self.startValue().srid if hasattr(self.startValue(), "srid") else None
		return result

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		if value[0] != '{' and value[0] != '[' and value[0] != '(':
			return TGeomPointInst(value)
		elif value[0] == '[' or value[0] == '(':
			return TGeomPointSeq(value)
		elif (value[0] == '{'):
			if value[1] == '[' or value[1] == '(':
				return TGeomPointS(value)
			else:
				return TGeomPointI(value)
		raise Exception("ERROR: Could not parse temporal float value")


class TGeomPointInst(TemporalInst, TGeomPoint):
	"""
	Temporal geometric points of instant duration
	"""

	def __init__(self, value, time=None):
		TemporalInst.BaseClass = Point
		#super().__init__(value, time)
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
			idx1 = value.find('(')
			idx2 = value.find(')')
			coords = (value[idx1 + 1:idx2]).split(' ')
			self._value = self.BaseClass(coords)
			self._time = parse(time)
		# Constructor with two arguments of type BaseClass and datetime
		elif isinstance(value, self.BaseClass) and isinstance(time, datetime):
			self._value = value
			self._time = time
		else:
			raise Exception("ERROR: Could not parse temporal instant value")
		# Verify validity of the resulting instance
		self._valid()

	def _valid(self):
		if self._value.m is not None:
			raise Exception("ERROR: The geometries composing a temporal point cannot have M dimension")

	def getValues(self):
		"""
		Distinct values
		"""
		return self._value


class TGeomPointI(TemporalI, TGeomPoint):
	"""
	Temporal geometric points of instant set duration
	"""

	def __init__(self,  *argv):
		TemporalI.BaseClass = Point
		TemporalI.ComponentClass = TGeomPointInst
		super().__init__(*argv)

	def _valid(self):
		super()._valid()
		if any((x._value.z is None and y._value.z is not None) or (x._value.z is not None and y._value.z is None) \
				for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: All geometries composing a temporal point must be of the same dimensionality")
		if any(x._value.m is not None for x in self._instantList):
			raise Exception("ERROR: The geometries composing a temporal point cannot have M dimension")
		if any(x.srid() != y.srid() for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: All geometries composing a temporal point must have the same SRID")

	def getValues(self):
		"""
		Distinct values
		"""
		values = super().getValues()
		return MultiPoint(values)


class TGeomPointSeq(TemporalSeq, TGeomPoint):
	"""
	Temporal geometric points of sequence duration
	"""

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseClass = Point
		TemporalSeq.ComponentClass = TGeomPointInst
		super().__init__(instantList, lower_inc, upper_inc)

	def _valid(self):
		super()._valid()
		if any((x._value.z is None and y._value.z is not None) or (x._value.z is not None and y._value.z is None) \
				for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: All geometries composing a temporal point must be of the same dimensionality")
		if any(x._value.m is not None for x in self._instantList):
			raise Exception("ERROR: The geometries composing a temporal point cannot have M dimension")
		if any(x.srid() != y.srid() for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: All geometries composing a temporal point must have the same SRID")

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


class TGeomPointS(TemporalS, TGeomPoint):
	"""
	Temporal geometric points of sequence set duration
	"""

	def __init__(self, *argv):
		TemporalS.BaseClass = Point
		TemporalS.ComponentClass = TGeomPointSeq
		super().__init__(*argv)

	def _valid(self):
		super()._valid()
		if any((x.has_z is None and y.has_z is not None) or (x.has_z is not None and y.has_z is None) \
				for x, y in zip(self._sequenceList, self._sequenceList[1:])):
			raise Exception("ERROR: All geometries composing a temporal point must be of the same dimensionality")
		if any(x.srid() != y.srid() for x, y in zip(self._sequenceList, self._sequenceList[1:])):
			raise Exception("ERROR: All geometries composing a temporal point must have the same SRID")

	def getValues(self):
		"""
		Distinct values
		"""
		values = [seq.getValues() for seq in self._sequenceList]
		points = [geom for geom in values if isinstance(geom, Point)]
		lines = [geom for geom in values if isinstance(geom, LineString)]
		if len(points) != 0 and len(points) != 0:
			return GeometryCollection(points + lines)
		if len(points) != 0 and len(points) == 0:
			return MultiPoint(points)
		if len(points) == 0 and len(points) != 0:
			return MultiLineString(lines)
