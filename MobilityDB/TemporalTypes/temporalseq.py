from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS
from postgis import Point, LineString


class TEMPORALSEQ(TEMPORALINSTANTS):
	Duration = 3

	def getDistinctValues(self, base=None):
		# Remove duplicates
		new_list = []
		for inst in self.value:
			if inst.value not in new_list:
				new_list.append(inst.value)

		if base == Point:
			if len(new_list) == 1:
				return Point(self.startInstant())
			else:
				return LineString(new_list)
		else:
			return new_list

	def __str__(self):
		return "{}[{}]".format("", self.getInstants())
