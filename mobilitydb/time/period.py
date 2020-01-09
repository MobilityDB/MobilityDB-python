import datetime
from dateutil.parser import parse
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class Period:
	"""
	Set of contiguous timestamps between a lower and an upper bound. The bounds may be inclusive or not
	"""
	__slots__ = ['_lower', '_upper', '_lower_inc', '_upper_inc']

	def __init__(self, lower, upper=None, lower_inc=None, upper_inc=None):
		assert(isinstance(lower_inc, (bool, type(None))))
		assert(isinstance(upper_inc, (bool, type(None))))
		# Constructor with a single argument of type string
		if upper is None and isinstance(lower, str):
			lower = lower.strip()
			assert(lower[0] == '[' or lower[0] == '('), "Lower bound flag must be either '[' or '('"
			assert(lower[-1] == ']' or lower[-1] == ')'), "Upper bound flag must be either ']' or ')'"
			self._lower_inc = True if lower[0] == '[' else False
			self._upper_inc = True if lower[-1] == ']' else False
			bounds = lower[1:-1].split(',')
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
		self._valid()

	def _valid(self):
		if self._lower > self._upper:
			raise Exception("ERROR: The lower bound must be less than or equal to the upper bound")
		if (self._lower == self._upper and
			(self._lower_inc == False or self._upper_inc == False)):
			raise Exception("ERROR: The lower and upper bounds must be inclusive for an instant period")
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
		return Period(self._lower + timedelta, self._upper + timedelta,
					  self._lower_inc, self._upper_inc)

	@staticmethod
	def _cmp_bounds(t1, t2, lower1, lower2, inclusive1, inclusive2):
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
				if lower1:
					return 1
				else:
					return -1
		elif not inclusive1:
			if lower1:
				return 1
			else:
				return -1
		elif not inclusive2:
			if lower2:
				return -1
			else:
				return 1
		else:
			return 0

	def overlap(self, other):
		"""
		Returns True if both period share any timestamps.
		"""
		if ((self._cmp_bounds(self._lower, other._lower, True, True, self._lower_inc, other._lower_inc) >= 0 and
					 self._cmp_bounds(self._lower, other._upper, True, False, self._lower_inc, other._upper_inc) <= 0) or
			(self._cmp_bounds(other._lower, self._lower, True, True, other._lower_inc, self._lower_inc) >= 0 and
					 self._cmp_bounds(other._lower, self._upper, True, False, other._lower_inc, self._upper_inc) <= 0)):
			return True
		return False

	def contains_timestamp(self, datetime):
		"""
		Returns True if the period contains the timestamp.
		"""
		if ((self._lower < datetime < self._upper) or
			(self._lower_inc and self._lower == datetime) or
			(self._upper_inc and self._upper == datetime)):
			return True
		return False

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if (self._lower == other._lower and self._upper == other._upper and
				self._lower_inc == other._lower_inc and self._upper_inc == other._upper_inc):
				return True
		return False

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

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return Period(value)

	@staticmethod
	def write(value):
		if not isinstance(value, Period):
			raise ValueError('Value must be an instance of Period class')
		return value.__str__().strip("'")

	def __str__(self):
		lower_str = '[' if self._lower_inc else '('
		upper_str = ']' if self._upper_inc else ')'
		return f"'{lower_str}{self._lower}, {self._upper}{upper_str}'"

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._lower!r}, {self._upper!r}, {self._lower_inc!r}, {self._upper_inc!r})')
