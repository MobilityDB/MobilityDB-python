import datetime
from bdateutil.parser import parse


def _period_cmp_bounds(t1, t2, lower1, lower2, inclusive1, inclusive2):
	# Compare the values
	if t1 < t2:
		return -1
	elif t1 > t2:
		return 1
	"""
	If the comparison is not equal and the bounds are both inclusive or 
	both exclusive, we're done. If they compare equal, we still have to 
	consider whether the boundaries are inclusive or exclusive. 
	"""
	if not inclusive1 and not inclusive2:
		# both are exclusive
		if lower1 == lower2:
			return 0
		else:
			result = 1 if lower1 else -1
			return result
	elif not inclusive1:
		result = 1 if lower1 else -1
		return result
	elif not inclusive2:
		result = -1 if lower2 else 1
		return result

class PERIOD:
	__slots__ = ['_lower', '_upper', '_lower_inc', '_upper_inc']

	def __init__(self, lower, upper=None, lower_inc=None, upper_inc=None):
		# Constructor with a single argument of type string
		if upper is None and isinstance(lower, str):
			lower = lower.strip()
			self._lower_inc = True if lower[0] == '[' else False
			self._upper_inc = True if lower[-1] == ']' else False
			bounds = lower.split(',')
			bounds[0] = (bounds[0])[1:]
			bounds[1] = (bounds[1])[:-1]
			self._lower = parse(bounds[0])
			self._upper = parse(bounds[1])
		# Constructor with two arguments of type string and optional arguments for the bounds
		elif isinstance(lower, str) and isinstance(upper, str):
			self._lower = parse(lower)
			self._upper = parse(upper)
			self._lower_inc = lower_inc if lower_inc is not None else True
			self._upper_inc = upper_inc if upper_inc is not None else False
		# Constructor with two arguments of type datetime and optional arguments for the bounds
		elif isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
			self._lower = lower
			self._upper = upper
			self._lower_inc = lower_inc if lower_inc is not None else True
			self._upper_inc = upper_inc if upper_inc is not None else False
		else:
			raise Exception("ERROR: Could not parse period value")
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: Invalid period arguments")

	def _valid(self):
		if self._lower > self._upper:
			return False
		if self._lower == self._upper and \
				(self._lower_inc == False or self._upper_inc == False):
			return False
		return True

	def lower(self):
		"""
		Lower bound
		"""
		return self._lower

	def upper(self):
		"""
		Upper bound
		"""
		return self._upper

	def lower_inc(self):
		"""
		Is the lower bound inclusive?
		"""
		return self._lower_inc

	def upper_inc(self):
		"""
		Is the upper bound inclusive?
		"""
		return self._upper_inc

	def timespan(self):
		"""
		Interval
		"""
		return self._upper - self._lower

	def shift(self, timedelta):
		"""
		Shift
		"""
		return PERIOD(self._lower + timedelta, self._upper + timedelta,
					  self._lower_inc, self._upper_inc)

	def overlap(self, other):
		"""
		Returns True if both ranges share any points.
		"""
		if _period_cmp_bounds(self._lower, other._lower, True, True, self._lower_inc, other._lower_inc) >= 0 and \
			_period_cmp_bounds(self._lower, other._upper, True, False, self._lower_inc, other._upper_inc) <= 0:
			return True

		if _period_cmp_bounds(other._lower, self._lower, True, True, other._lower_inc, self._lower_inc) >= 0 and \
			_period_cmp_bounds(other._lower, self._upper, True, False, other._lower_inc, self._upper_inc) <= 0:
			return True
		return False

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self._lower != other._lower or self._upper != other._upper or \
							self._lower_inc != other._lower_inc or self._upper_inc != other._upper_inc:
				return False
		return True

	def _cmp(self, other):
		if isinstance(other, self.__class__):
			if self._lower < other._lower:
				return -1
			elif self._lower > other._lower:
				return 1
			elif self._upper < other._upper:
				return -1
			elif self._upper > other._upper:
				return 1
			elif self._lower_inc and not other._lower_inc:
				return -1
			elif not self._lower_inc and other._lower_inc:
				return 1
			elif self._upper_inc and not other._upper_inc:
				return -1
			elif not self._upper_inc and other._upper_inc:
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
		lower_str = '[' if self._lower_inc else '('
		upper_str = ']' if self._upper_inc else ')'
		return "'" + lower_str + '{}, {}'.format(self._lower, self._upper) + upper_str + "'"

	# TODO
	# def __repr__(self):
