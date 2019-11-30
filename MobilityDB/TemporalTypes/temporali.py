from MobilityDB.TemporalTypes.temporalinst import TemporalInst
from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS
from MobilityDB.TimeTypes.period import Period
from MobilityDB.TimeTypes.periodset import PeriodSet


class TemporalI(TEMPORALINSTANTS):
	"""
	Abstract class for temporal types of instant set duration
	"""

	def __init__(self, *argv):
		# Constructor with a single argument of type string
		self._instantList = []
		if len(argv) == 1 and isinstance(argv[0], str):
			ts = argv[0].strip()
			if ts[0] == '{' and ts[-1] == '}':
				ts = ts[1:-1]
				instants = ts.split(",")
				for inst in instants:
					self._instantList.append(TemporalI.ComponentClass(inst.strip()))
			else:
				raise Exception("ERROR: Could not parse temporal instant set value")
		# Constructor with a single argument of type list
		elif len(argv) == 1 and isinstance(argv[0], list):
			# List of strings representing instant values
			if all(isinstance(arg, str) for arg in argv[0]):
				for arg in argv[0]:
					self._instantList.append(TemporalI.ComponentClass(arg))
			# List of instant values
			elif all(isinstance(arg, TemporalI.ComponentClass) for arg in argv[0]):
				for arg in argv[0]:
					self._instantList.append(arg)
			else:
				raise Exception("ERROR: Could not parse temporal instant set value")
		# Constructor with multiple arguments
		else:
			# Arguments are of type string
			if all(isinstance(arg, str) for arg in argv):
				for arg in argv:
					self._instantList.append(TemporalI.ComponentClass(arg))
			# Arguments are of type instant
			elif all(isinstance(arg, TemporalI.ComponentClass) for arg in argv):
				for arg in argv:
					self._instantList.append(arg)
			else:
				raise Exception("ERROR: Could not parse temporal instant set value")
		# Verify validity of the resulting instance
		self._valid()

	def _valid(self):
		if any(x._time > y._time for x, y in zip(self._instantList, self._instantList[1:])):
			raise Exception("ERROR: The timestamps of a temporal instant must be increasing")

	@classmethod
	def duration(cls):
		return "InstantSet"

	def getTime(self):
		"""
		Timestamp
		"""
		return PeriodSet([Period(inst._time, inst._time, True, True) for inst in self._instantList])

	def period(self):
		"""
		Period on which the temporal value is defined
		"""
		return Period(self.startTimestamp(), self.endTimestamp(), True, True)

	def intersectsTimestamp(self, timestamp):
		"""
		Intersects timestamp
		"""
		return any(inst._time == timestamp for inst in self._instantList)

	def intersectsTimestampset(self, timestampset):
		"""
		Intersects timestamp set
		"""
		return any(inst._time == timestamp for inst in self._instantList for timestamp in timestampset._datetimeList)

	def intersectsPeriod(self, period):
		"""
		Intersects period
		"""
		return any(period.contains_timestamp(inst._time) for inst in self._instantList)

	def intersectsPeriodset(self, periodset):
		"""
		Intersects period set
		"""
		return any(period.contains_timestamp(inst._time) for inst in self._instantList for period in periodset._periodList)

	def __str__(self):
		return "'{" + TEMPORALINSTANTS.__str__(self) + "}'"
