from datetime import datetime
from dateutil.parser import parse
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class TBox:
	__slots__ = ['_xmin', '_tmin', '_xmax', '_tmax']

	def __init__(self, *args):
		print("*** args", args)
		if len(args) == 1 and isinstance(args[0], str):
			self.parseFromString(args[0])
		elif len(args) == 2:
			if isinstance(args[0], str) and isinstance(args[1], str):
				try:
					self._xmin = float(args[0])
					self._xmax = float(args[1])
					self._tmin = self._tmax = None
				except:
					self._tmin = parse(args[0])
					self._tmax = parse(args[1])
					self._xmin = self._xmax = None
			elif isinstance(args[0], float) and isinstance(args[1], float):
				self._xmin = args[0]
				self._xmax = args[1]
				self._tmin = self._tmax = None
			elif isinstance(args[0], datetime) and isinstance(args[1], datetime):
				self._tmin = args[0]
				self._tmax = args[1]
				self._xmin = self._xmax = None
			else:
				raise Exception("ERROR: Cannot parse TBox")
		elif len(args) == 4:
			self._xmin = float(args[0])
			self._xmax = float(args[2])
			if isinstance(args[1], str) and isinstance(args[3], str):
				self._tmin = parse(args[1])
				self._tmax = parse(args[3])
			elif isinstance(args[1], datetime) and isinstance(args[3], datetime):
				self._tmin = args[1]
				self._tmax = args[3]
			else:
				raise Exception("ERROR: Cannot parse TBox")
		else:
			raise Exception("ERROR: Cannot parse TBox")

	def parseFromString(self, value):
		values = value.replace("TBOX", '')
		if 'T' in values:
			time = True
			self._xmin = None
			self._xmax = None
		else:
			time = False
		values = values.replace('T', '').replace('(', '').replace(')', '').split(',')
		if time:
			self._tmin = parse(values[0])
			self._tmax = parse(values[1])
		elif len(values) == 4:
			self._xmin = float(values[0]) if values[0] != '' and not values[0].isspace() else None
			self._xmax = float(values[2]) if values[2] != '' and not values[2].isspace() else None
			self._tmin = parse(values[1]) if values[1] != '' and not values[1].isspace() else None
			self._tmax = parse(values[3]) if values[3] != '' and not values[3].isspace() else None
		else:
			raise Exception("ERROR: Cannot parse TBox")

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return TBox(value)

	@staticmethod
	def write(value):
		if not isinstance(value, TBox):
			raise ValueError('Value must be instance of TBox class')
		return value.__str__().strip("'")

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

	def xmin(self):
		"""
		Minimum x
		"""
		return self._xmin

	def tmin(self):
		"""
		Minimum t
		"""
		return self._tmin

	def xmax(self):
		"""
		Maximum x
		"""
		return self._xmax

	def tmax(self):
		"""
		Maximum t
		"""
		return self._tmax

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self._xmin == other._xmin and self._tmin == other._tmin and self._xmax == other._xmax and \
				self._tmax == other._tmax
		return False

	def __str__(self):
		if self._xmin is not None and self._tmin is not None:
			return "'TBOX((%s, %s), (%s, %s))'" % (repr(self._xmin), self._tmin, repr(self._xmax), self._tmax)
		elif self._xmin is not None:
			return "'TBOX((%s, ), (%s, ))'" % (repr(self._xmin), repr(self._xmax))
		elif self._tmin is not None:
			return "'TBOX((, %s), (, %s))'" % (self._tmin, self._tmax)

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._xmin!r}, {self._tmin!r}, {self._xmax!r}, {self._tmax!r})')

