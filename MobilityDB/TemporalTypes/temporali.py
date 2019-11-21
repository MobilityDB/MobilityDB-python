from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS
from MobilityDB.TimeTypes.period import PERIOD

class TEMPORALI(TEMPORALINSTANTS):
	Duration = 2

	@classmethod
	def duration(cls):
		return "InstantSet"

	def period(self):
		"""
		Period on which the temporal value is defined
		"""
		return PERIOD(self.startTimestap(), self.endTimestap(), True, True)

	def __str__(self):
		return '{' + TEMPORALINSTANTS.__str__(self) + '}'
