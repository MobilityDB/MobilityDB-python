from postgis import Point
from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TGeogPoint(Temporal):
	BaseValueClass = Point
	SRID = 0

	def __init__(self, value=None, srid=None):
		if isinstance(value, str):
			self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
			if srid is not None:
				self.SRID = srid
			else:
				self.SRID = 0
		elif isinstance(value, list):
			try:
				listItems = []
				for item in value:
					if isinstance(item, self.SubClass.__class__.__bases__[0]):
						listItems.append(item.SubClass)
				if value[0].SubClass.__class__ == TemporalInst:
					self.SubClass = TemporalI(listItems)
				elif value[0].SubClass.__class__ == TemporalSeq:
					self.SubClass = TemporalS(listItems)
			except:
				raise Exception("ERROR: different types")
		else:
			self.SubClass = value

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return TGeogPoint(MobilityDBReader.readTemporalType(TGeogPoint, value))

	def __str__(self):
		if len(self.__class__.__bases__) == 2:
			if self.SRID != 0:
				return self.__class__.__bases__[0].__name__ + " 'SRID=" + str(
					self.SRID) + ";" + self.SubClass.__str__() + "'"
			else:
				return self.__class__.__bases__[0].__name__ + " '" + self.SubClass.__str__() + "'"
		else:
			if self.SRID != 0:
				return self.__class__.__name__ + " 'SRID=" + str(self.SRID) + ";" + self.SubClass.__str__() + "'"
			else:
				return self.__class__.__name__ + " '" + self.SubClass.__str__() + "'"


class TGeogPointInst(TGeogPoint, TemporalInst):
	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalInst:
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal instant")


class TGeogPointI(TGeogPoint, TemporalI):
	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalI or isinstance(value, list):
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal instant set")


class TGeogPointSeq(TGeogPoint, TemporalSeq):
	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalSeq:
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal sequence")


class TGeogPointS(TGeogPoint, TemporalS):
	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalS or isinstance(value, list):
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal sequence set")
