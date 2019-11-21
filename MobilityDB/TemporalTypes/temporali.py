from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS


class TEMPORALI(TEMPORALINSTANTS):
	Duration = 2

	@classmethod
	def getType(cls):
		return "InstantSet"

	def period(self):
		"""

		"""
		return PERIOD(self.startTimestap(), self.endTimestap(), True, True)

	def __str__(self):
		return "{}{{{}}}".format("", self.getInstants())
