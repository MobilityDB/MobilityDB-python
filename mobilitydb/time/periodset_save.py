from .period import Period
import re


class PeriodSet:
	__slots__ = ['periodList']

	def __init__(self, *argv):
		self.periodList = []
		# Constructor with a single argument of type string
		if len(argv) == 1 and isinstance(argv[0], str):
			ps = argv[0].strip()
			if ps[0] == '{' and ps[-1] == '}':
				p = re.compile('[\[|\(].*?[^\]\)][\]|\)]')
				periods = p.findall(ps)
				for period in periods:
					self.periodList.append(Period(period))
			else:
				raise Exception("ERROR: Could not parse period set value")
		# Constructor with a single argument of type list
		elif len(argv) == 1 and isinstance(argv[0], list):
			# List of strings representing periods
			if all(isinstance(arg, str) for arg in argv[0]):
				for arg in argv[0]:
					self.periodList.append(Period(arg))
			# List of periods
			elif all(isinstance(arg, Period) for arg in argv[0]):
				for arg in argv[0]:
					self.periodList.append(arg)
			else:
				raise Exception("ERROR: Could not parse period set value")
		# Constructor with multiple arguments
		else:
			# Arguments are of type string
			if all(isinstance(arg, str) for arg in argv):
				for arg in argv:
					self.periodList.append(Period(arg))
			# Arguments are of type period
			elif all(isinstance(arg, Period) for arg in argv):
				for arg in argv:
					self.periodList.append(arg)
			else:
				raise Exception("ERROR: Could not parse period set value")
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: Invalid period arguments")

	def _valid(self):
		return all(x.upperBound < y.lowerBound or \
				   (x.upperBound == y.lowerBound and (not x.upperBound_inc or not x.lowerBound_inc)) \
				   for x, y in zip(self.periodList, self.periodList[1:]))

	def timespan(self):
		"""
		Interval
		"""
		return self.endTimestamp() - self.startTimestamp()

	def period(self):
		"""
		Period on which the period set is defined ignoring the potential time gaps
        """
		return Period((self.periodList[0]).lowerBound, (self.periodList[-1]).lowerBound,
					  self.periodList[0].lowerBound_inc, self.periodList[-1].lowerBound_inc)

	def numTimestamps(self):
		"""
		Number of distinct timestamps
		"""
		return len(self.timestamps())

	def startTimestamp(self):
		"""
		Start timestamp
		"""
		return self.periodList[0].lowerBound

	def endTimestamp(self):
		"""
		End timestamp
		"""
		return self.periodList[-1].upperBound

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
		for period in self.periodList:
			timestampList.append(period.lowerBound)
			timestampList.append(period.upperBound)
		# Remove duplicates
		timestampList = list(dict.fromkeys(timestampList))
		return timestampList

	def numPeriods(self):
		"""
		Number of periods
		"""
		return len(self.periodList)

	def startPeriod(self):
		"""
		Start period
		"""
		return self.periodList[0]

	def endPeriod(self):
		"""
		End period
		"""
		return self.periodList[self.numPeriods() - 1]

	def periodN(self, n):
		"""
		N-th period
		"""
		if 0 <= n < len(self.periodList):
			return self.periodList[n]
		else:
			raise Exception("ERROR: Out of range")

	def periods(self):
		"""
		Periods
		"""
		return [period for period in self.periodList]

	def shift(self, timedelta):
		"""
		Shift
		"""
		return PeriodSet([period.shift(timedelta) for period in self.periodList])

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if len(other.periodList) == len(self.periodList) and set(other.periodList).intersection(self.periodList):
				return True
		return False

	def __str__(self):
		return "'{{{}}}'".format(', '.join('{}'.format(period.__str__().replace("'", ""))
										   for period in self.periodList))
