from postgis import Point
from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TGEOMPOINT(TEMPORAL):
	"""
	A representation of TGEOMPOINT.

	TGEOMPOINT is used to represent the evolution of a geometry point over time, e.g., a vehicle trajectory.
	It comes in four durations (Instant, Instant Set, Sequence, Sequence Set).
		>>> TGEOMPOINT("srid=4326;Point(1 1)@2019-09-08")
		>>> TGEOMPOINT("srid=4326;{Point(1 1)@2019-09-08, Point(2 2)@2019-09-09}")
		>>> TGEOMPOINT("srid=4326;[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09]")
		>>> TGEOMPOINT("srid=4326;{[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09],[Point(3 3)@2019-09-10]}")
	"""
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
				if value[0].SubClass.__class__ == TEMPORALINST:
					self.SubClass = TEMPORALI(listItems)
				elif value[0].SubClass.__class__ == TEMPORALSEQ:
					self.SubClass = TEMPORALS(listItems)
			except:
				raise Exception("ERROR: different types")
		else:
			self.SubClass = value

	@staticmethod
	def read_from_cursor(value, cursor=None):
		"""
		Create a TGEOMPOINT object from the value returned from the cursor. The reader accepts any subclass of
		TGEOMPOINT.
		"""
		if not value:
			return None
		return TGEOMPOINT(MobilityDBReader.readTemporalType(TGEOMPOINT, value))

	def __str__(self):
		if len(self.__class__.__bases__) == 2:
			if self.SRID != 0:
				return self.__class__.__bases__[0].__name__ + " 'SRID=" + str(self.SRID) + ";" + \
					   self.SubClass.__str__() + "'"
			else:
				return self.__class__.__bases__[0].__name__ + " '" + self.SubClass.__str__() + "'"
		else:
			if self.SRID != 0:
				return self.__class__.__name__ + " 'SRID=" + str(self.SRID) + ";" + self.SubClass.__str__() + "'"
			else:
				return self.__class__.__name__ + "'" + self.SubClass.__str__() + "'"


class TGEOMPOINTINST(TGEOMPOINT, TEMPORALINST):
	"""
	A representation of TGEOMPOINTINST.

	TGEOMPOINTINST is used to represent a temporal point of instant duration.
		>>> TGEOMPOINTINST("srid=4326;Point(1 1)@2019-09-08")
			<TGEOMPOINTINST: 'TGEOMPOINT(Instant, Point, 4326)'>
		>>> TGEOMPOINTINST("srid=4326;Point(1 1 1)@2019-09-08")
			<TGEOMPOINTINST: 'TGEOMPOINT(Instant, PointZ, 4326)'>
	"""

	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TEMPORALINST:
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal instant")


class TGEOMPOINTI(TGEOMPOINT, TEMPORALI):
	"""
	A representation of TGEOMPOINTI.

	TGEOMPOINTI is used to represent a set of discrete instants.
		>>> TGEOMPOINTI("srid=4326;{Point(1 1)@2019-09-08, Point(2 2)@2019-09-09}")
			<TGEOMPOINTI: 'TGEOMPOINT(InstantSet, Point, 4326)'>
	"""

	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TEMPORALI or isinstance(value, list):
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal instant set")


class TGEOMPOINTSEQ(TGEOMPOINT, TEMPORALSEQ):
	"""
	A representation of TGEOMPOINTSEQ.

	TGEOMPOINTSEQ is used to represent a set of connected instants.
		>>> TGEOMPOINTSEQ("srid=4326;[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09]")
			<TGEOMPOINTSEQ: 'TGEOMPOINT(Sequence, Point, 4326)'>
	"""

	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TEMPORALSEQ:
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal sequence")


class TGEOMPOINTS(TGEOMPOINT, TEMPORALS):
	"""
	A representation of TGEOMPOINTS.

	TGEOMPOINTS is used to represent a set of sequences.
		>>> TGEOMPOINTS("srid=4326;{[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09],[Point(3 3)@2019-09-10]}")
			<TGEOMPOINTS: 'TGEOMPOINT(SequenceSet, Point, 4326)'>
	"""

	def __init__(self, value=None, srid=None):
		if MobilityDBReader.checkTemporalType(value) == TEMPORALS or isinstance(value, list):
			super().__init__(value, srid)
		else:
			raise Exception("ERROR: Input must be a temporal sequence set")
