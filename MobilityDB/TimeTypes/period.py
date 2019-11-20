import datetime
from bdateutil.parser import parse

class PERIOD:
	__slots__ = ['lowerBound', 'upperBound', 'lowerBound_inc', 'upperBound_inc']

	def __init__(self, lower, upper=None, lower_inc=None, upper_inc=None):
		# Constructor with a single argument of type string
		if upper is None and isinstance(lower, str):
			lower = lower.strip()
			self.lowerBound_inc = True if lower[0] == '[' else False
			self.upperBound_inc = True if lower[len(lower) - 1] == ']' else False
			bounds = lower.split(',')
			bounds[0] = (bounds[0])[1:]
			bounds[1] = (bounds[1])[:-1]
			self.lowerBound = parse(bounds[0])
			self.upperBound = parse(bounds[1])
		# Constructor with two arguments of type string and optional arguments for the bounds
		elif isinstance(lower, str) and isinstance(upper, str):
			self.lowerBound = parse(lower)
			self.upperBound = parse(upper)
			self.lowerBound_inc = lower_inc if lower_inc is not None else True
			self.upperBound_inc = upper_inc if upper_inc is not None else False
		# Constructor with two arguments of type datetime and optional arguments for the bounds
		elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
			self.lowerBound = lower
			self.upperBound = upper
			self.lowerBound_inc = lower_inc if lower_inc is not None else True
			self.upperBound_inc = upper_inc if upper_inc is not None else False
		else:
			raise Exception("ERROR: Could not parse period value")
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: Invalid period arguments")

	def _valid(self):
		if self.lowerBound > self.upperBound:
			return False
		if self.lowerBound == self.upperBound and \
			(self.lowerBound_inc == False or self.upperBound_inc == False):
			return False
		return True

	def lower(self):
		"""
		Lower bound
		"""
		return self.lowerBound

	def upper(self):
		"""
		Upper bound
		"""
		return self.upperBound

	def lower_inc(self):
		"""
		Is the lower bound inclusive?
		"""
		return self.lowerBound_inc

	def upper_inc(self):
		"""
		Is the upper bound inclusive?
		"""
		return self.upperBound_inc

	def timespan(self):
		"""
		Interval
		"""
		return self.upperBound - self.lowerBound

	def shift(self, timedelta):
		"""
		Shift
		"""
		return PERIOD(self.lowerBound + timedelta, self.upperBound + timedelta,
			self.lowerBound_inc, self.upperBound_inc)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self.lowerBound != other.lowerBound or self.upperBound != other.upperBound or \
							self.lowerBound_inc != other.lowerBound_inc or self.upperBound_inc != other.upperBound_inc:
				return False
		return True

	def _cmp(self, other):
		if isinstance(other, self.__class__):
			if self.lowerBound < other.lowerBound:
				return -1
			elif self.lowerBound > other.lowerBound:
				return 1
			elif self.upperBound < other.upperBound:
				return -1
			elif self.upperBound > other.upperBound:
				return 1
			elif self.lowerBound_inc and not other.lowerBound_inc:
				return -1
			elif not self.lowerBound_inc and other.lowerBound_inc:
				return 1
			elif self.upperBound_inc and not other.upperBound_inc:
				return -1
			elif not self.upperBound_inc and other.upperBound_inc:
				return 1
			return 0

	def __lt__(self, other):
		if isinstance(other, self.__class__):
			if self._cmp(other) == -1:
				return True
			return False

	def __le__(self, other):
		if isinstance(other, self.__class__):
			if self._cmp(other) == -1 or self._cmp(other) == 0:
				return True
			return False

	def __gt__(self, other):
		if isinstance(other, self.__class__):
			if self._cmp(other) == 1:
				return True
			return False

	def __ge__(self, other):
		if isinstance(other, self.__class__):
			if self._cmp(other) == 1 or self._cmp(other) == 0:
				return True
			return False

	def __str__(self):
		lower_str = '[' if self.lowerBound_inc else '('
		upper_str = ']' if self.upperBound_inc else ')'
		return "'" + lower_str + '{}, {}'.format(self.lowerBound, self.upperBound) + upper_str + "'"

	# TODO
	#def __repr__(self):
