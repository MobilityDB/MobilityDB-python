from MobilityDB.TemporalTypes import *
from MobilityDB.MobilityDBReader import MobilityDBReader


class TBool(Temporal):
	BaseClass = bool

	def __init__(self, value=None):
		if isinstance(value, str):
			self.SubClass = MobilityDBReader.readTemporalType(self.__class__, value)
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
		return TBool(MobilityDBReader.readTemporalType(TBool, value))


class TBoolInst(TBool, TemporalInst):
	def __init__(self, value=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalInst:
			super().__init__(value)
		else:
			raise Exception("ERROR: Input must be a temporal instant")


class TBoolI(TBool, TemporalI):
	def __init__(self, value=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalI or isinstance(value, list):
			super().__init__(value)
		else:
			raise Exception("ERROR: Input must be a temporal instant set")


class TBoolSeq(TBool, TemporalSeq):
	def __init__(self, value=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalSeq:
			super().__init__(value)
		else:
			raise Exception("ERROR: Input must be a temporal sequence")


class TBoolS(TBool, TemporalS):
	def __init__(self, value=None):
		if MobilityDBReader.checkTemporalType(value) == TemporalS or isinstance(value, list):
			super().__init__(value)
		else:
			raise Exception("ERROR: Input must be a temporal sequence set")
