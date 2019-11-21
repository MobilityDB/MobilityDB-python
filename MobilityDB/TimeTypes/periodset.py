from .period import PERIOD
import re


class PERIODSET:
	__slots__ = ['_periodList']

	def __init__(self, *argv):
		self._periodList = []
		# Constructor with a single argument of type string
		if len(argv) == 1 and isinstance(argv[0], str):
			ps = argv[0].strip()
			if ps[0] == '{' and ps[-1] == '}':
				p = re.compile('[\[|\(].*?[^\]\)][\]|\)]')
				periods = p.findall(ps)
				for period in periods:
					self._periodList.append(PERIOD(period))
			else:
				raise Exception("ERROR: Could not parse period set value")
		# Constructor with a single argument of type list
		elif len(argv) == 1 and isinstance(argv[0], list):
			# List of strings representing periods
			if all(isinstance(arg, str) for arg in argv[0]):
				for arg in argv[0]:
					self._periodList.append(PERIOD(arg))
			# List of periods
			elif all(isinstance(arg, PERIOD) for arg in argv[0]):
				for arg in argv[0]:
					self._periodList.append(arg)
			else:
				raise Exception("ERROR: Could not parse period set value")
		# Constructor with multiple arguments
		else:
			# Arguments are of type string
			if all(isinstance(arg, str) for arg in argv):
				for arg in argv:
					self._periodList.append(PERIOD(arg))
			# Arguments are of type period
			elif all(isinstance(arg, PERIOD) for arg in argv):
				for arg in argv:
					self._periodList.append(arg)
			else:
				raise Exception("ERROR: Could not parse period set value")
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: Invalid period arguments")

	def _valid(self):
		return all(x.upper() < y.lower() or \
			(x.upper() == y.lower() and (not x.upper_inc() or not x.lower_inc())) \
				   for x, y in zip(self._periodList, self._periodList[1:]))

	def timespan(self):
		"""
		Interval
		"""
		return self.endTimestamp() - self.startTimestamp()

	def period(self):
		"""
		Period on which the period set is defined ignoring the potential time gaps
		"""
		return PERIOD((self._periodList[0]).lower(), (self._periodList[-1]).lower(),
					  self._periodList[0].lower_inc(), self._periodList[-1].lower_inc())

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self.timestamps())

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self._periodList[0].lower()

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self._periodList[-1].upper()

	def timestampN(self, n):
		"""
		N-th distinct timestamp
		"""
		# 1-based
		if 0 < n <= len(self.timestamps()):
			return (self.timestamps())[n - 1]
		else:
			raise Exception("ERROR: there is no value at this index")

	def timestamps(self):
		"""
		Distinct timestamps
		"""
		timestampList = []
		for period in self._periodList:
			timestampList.append(period.lower())
			timestampList.append(period.upper())
		# Remove duplicates
		timestampList = list(dict.fromkeys(timestampList))
		return timestampList

	def numPeriods(self):
		"""
		Number of periods
		"""
		return len(self._periodList)

	def startPeriod(self):
		"""
		Start period
		"""
		return self._periodList[0]

	def endPeriod(self):
		"""
		End period
		"""
		return self._periodList[self.numPeriods() - 1]

	def periodN(self, n):
		"""
		N-th period
		"""
		# 1-based
		if 0 <= n < len(self._periodList):
			return self._periodList[n - 1]
		else:
			raise Exception("ERROR: Out of range")

	def periods(self):
		"""
		Periods
		"""
		return [period for period in self._periodList]

	def shift(self, timedelta):
		"""
		Shift
		"""
		return PERIODSET([period.shift(timedelta) for period in self._periodList])

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if len(other._periodList) == len(self._periodList) and set(other._periodList).intersection(
					self._periodList):
				return True
		return False

	def __str__(self):
		return "'{{{}}}'".format(', '.join('{}'.format(period.__str__().replace("'", ""))
										   for period in self._periodList))
