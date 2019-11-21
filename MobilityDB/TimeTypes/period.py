import datetime
from bdateutil.parser import parse


class PERIOD:
	__slots__ = ['_lowerBound', '_upperBound', '_lowerBound_inc', '_upperBound_inc']

	def __init__(self, lower, upper=None, lower_inc=None, upper_inc=None):
		# Constructor with a single argument of type string
		if upper is None and isinstance(lower, str):
			lower = lower.strip()
			self._lowerBound_inc = True if lower[0] == '[' else False
			self._upperBound_inc = True if lower[len(lower) - 1] == ']' else False
			bounds = lower.split(',')
			bounds[0] = (bounds[0])[1:]
			bounds[1] = (bounds[1])[:-1]
			self._lowerBound = parse(bounds[0])
			self._upperBound = parse(bounds[1])
		# Constructor with two arguments of type string and optional arguments for the bounds
		elif isinstance(lower, str) and isinstance(upper, str):
			self._lowerBound = parse(lower)
			self._upperBound = parse(upper)
			self._lowerBound_inc = lower_inc if lower_inc is not None else True
			self._upperBound_inc = upper_inc if upper_inc is not None else False
		# Constructor with two arguments of type datetime and optional arguments for the bounds
		elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
			self._lowerBound = lower
			self._upperBound = upper
			self._lowerBound_inc = lower_inc if lower_inc is not None else True
			self._upperBound_inc = upper_inc if upper_inc is not None else False
		else:
			raise Exception("ERROR: Could not parse period value")
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: Invalid period arguments")

	def _valid(self):
		if self._lowerBound > self._upperBound:
			return False
		if self._lowerBound == self._upperBound and \
				(self._lowerBound_inc == False or self._upperBound_inc == False):
			return False
		return True

	def lower(self):
		"""
		Lower bound
		"""
		return self._lowerBound

	def upper(self):
		"""
		Upper bound
		"""
		return self._upperBound

	def lower_inc(self):
		"""
		Is the lower bound inclusive?
		"""
		return self._lowerBound_inc

	def upper_inc(self):
		"""
		Is the upper bound inclusive?
		"""
		return self._upperBound_inc

	def timespan(self):
		"""
		Interval
		"""
		return self._upperBound - self._lowerBound

	def shift(self, timedelta):
		"""
		Shift
		"""
		return PERIOD(self._lowerBound + timedelta, self._upperBound + timedelta,
					  self._lowerBound_inc, self._upperBound_inc)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._lowerBound != other._lowerBound or self._upperBound != other._upperBound or \
							self._lowerBound_inc != other._lowerBound_inc or self._upperBound_inc != other._upperBound_inc:
				return False
		return True

	def _cmp(self, other):
		if isinstance(other, self.__class__):
			if self._lowerBound < other._lowerBound:
				return -1
			elif self._lowerBound > other._lowerBound:
				return 1
			elif self._upperBound < other._upperBound:
				return -1
			elif self._upperBound > other._upperBound:
				return 1
			elif self._lowerBound_inc and not other._lowerBound_inc:
				return -1
			elif not self._lowerBound_inc and other._lowerBound_inc:
				return 1
			elif self._upperBound_inc and not other._upperBound_inc:
				return -1
			elif not self._upperBound_inc and other._upperBound_inc:
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
		lower_str = '[' if self._lowerBound_inc else '('
		upper_str = ']' if self._upperBound_inc else ')'
		return "'" + lower_str + '{}, {}'.format(self._lowerBound, self._upperBound) + upper_str + "'"

	# TODO
	# def __repr__(self):
