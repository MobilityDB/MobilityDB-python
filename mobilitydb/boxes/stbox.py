from datetime import datetime
from dateutil.parser import parse
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class STBox:
	__slots__ = ['_xmin', '_ymin', '_zmin', '_tmin', '_xmax', '_ymax', '_zmax', '_tmax', '_geodetic']

	def __init__(self, *args,  geodetic=None):
		# Initialize arguments to None
		self._xmin = self._xmax = self._ymin = self._ymax = self._zmin = self._zmax = self._tmin = self._tmax = None
		self._geodetic = geodetic if geodetic is not None else False
		# Index of the middle of the list of arguments
		half = int(len(args) / 2)
		if len(args) == 1 and isinstance(args[0], str):
			self.parseFromString(args[0])
		elif len(args) == 2:
			if isinstance(args[0], str) and isinstance(args[1], str):
				self._tmin = parse(args[0])
				self._tmax = parse(args[1])
			elif isinstance(args[0], datetime) and isinstance(args[1], datetime):
				self._tmin = args[0]
				self._tmax = args[1]
			else:
				raise Exception("ERROR: Cannot parse STBox")
		elif len(args) >= 4:
			self._xmin = float(args[0])
			self._xmax = float(args[half])
			self._ymin = float(args[1])
			self._ymax = float(args[half + 1])
		elif len(args) >= 6:
			if isinstance(args[2], str) and isinstance(args[half + 2], str):
				try:
					self._zmin = float(args[2])
					self._zmax = float(args[half + 2])
				except:
					self._tmin = parse(args[2])
					self._tmax = parse(args[half + 2])
			elif isinstance(args[2], float) and isinstance(args[half + 2], float):
				self._zmin = float(args[2])
				self._zmax = float(args[half + 2])
			elif isinstance(args[2], datetime) and isinstance(args[half + 2], datetime):
				self._tmin = args[2]
				self._tmax = args[half + 2]
			else:
				raise Exception("ERROR: Cannot parse STBox")
		elif len(args) == 8:
			if isinstance(args[3], str) and isinstance(args[7], str):
				self._tmin = parse(args[3])
				self._tmax = parse(args[7])
			elif isinstance(args[3], datetime) and isinstance(args[7], datetime):
				self._tmin = args[3]
				self._tmax = args[7]
			else:
				raise Exception("ERROR: Cannot parse STBox")
		else:
			raise Exception("ERROR: Cannot parse STBox")

	def parseFromString(self, value):
		if value is None or not isinstance(value, str):
			raise Exception("ERROR: Cannot parse STBox")
		values = None
		if 'GEODSTBOX' in value:
			self._geodetic = True
			value = value.replace("GEODSTBOX", '')
			hasz = True
			hast = True if 'T' in value else False
		elif 'STBOX' in value:
			value = value.replace("STBOX", '')
			hasz = True if 'Z' in value else False
			hast = True if 'T' in value else False
		else:
			raise Exception("ERROR: Input must be STBOX")
		values = value.replace('Z', '').replace('T', ''). replace('(', '').replace(')', '').split(',')
		# Remove empty or only space strings
		values = [value for value in values if value != '' and not value.isspace()]
		if len(values) == 2:
			self._tmin = parse(values[0])
			self._tmax = parse(values[1])
		else:
			if len(values) >= 4:
				self._xmin = float(values[0])
				self._xmax = float(values[int(len(values) / 2)])
				self._ymin = float(values[1])
				self._ymax = float(values[1 + int(len(values) / 2)])
			if hasz:
				self._zmin = float(values[2])
				self._zmax = float(values[2 + int(len(values) / 2)])
			if hast:
				self._tmin = parse(values[int(len(values) / 2) - 1])
				self._tmax = parse(values[(int(len(values) / 2) - 1) + int(len(values) / 2)])

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return STBox(value)

	@staticmethod
	def write(value):
		if not isinstance(value, STBox):
			raise ValueError('Value must be instance of STBox class')
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

	def ymin(self):
		"""
		Minimum y
		"""
		return self._ymin

	def zmin(self):
		"""
		Minimum z
		"""
		return self._ymin

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

	def ymax(self):
		"""
		Maximum y
		"""
		return self._ymax

	def zmax(self):
		"""
		Maximum y
		"""
		return self._zmax

	def tmax(self):
		"""
		Maximum t
		"""
		return self._tmax

	def geodetic(self):
		"""
		Maximum t
		"""
		return self._geodetic

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self._xmin == other._xmin and self._ymin == other._ymin and self._zmin == other._zmin and \
				   self._tmin == other._tmin and self._xmax == other._xmax and self._ymax == other._ymax and \
				   self._zmax == other._zmax and self._tmax == other._tmax and self._geodetic == other._geodetic
		return False

	def __str__(self):
		if self._geodetic:
			if self._tmin is not None:
				if self._xmin is not None:
					return "'GEODSTBOX T((%s, %s, %s, %s), (%s, %s, %s, %s))'" % \
						(self._xmin, self._ymin, self._zmin, self._tmin, self._xmax, self._ymax, self._zmax, self._tmax)
				else:
					return "'GEODSTBOX T((, %s), (, %s))'" % (self._tmin, self._tmax)
			else:
				return "'GEODSTBOX((%s, %s, %s), (%s, %s, %s))'" % \
					(self._xmin, self._ymin, self._zmin, self._xmax, self._ymax, self._zmax)
		else:
			if self._xmin is not None and self._zmin is not None and self._tmin is not None:
				return "'STBOX ZT((%s, %s, %s, %s), (%s, %s, %s, %s))'" % \
					(self._xmin, self._ymin, self._zmin, self._tmin, self._xmax, self._ymax, self._zmax, self._tmax)
			elif self._xmin is not None and self._zmin is not None and self._tmin is None:
				return "'STBOX Z((%s, %s, %s), (%s, %s, %s))'" % \
					(self._xmin, self._ymin, self._zmin, self._xmax, self._ymax, self._zmax)
			elif self._xmin is not None and self._zmin is None and self._tmin is not None:
				return "'STBOX T((%s, %s, %s), (%s, %s, %s))'" % \
					(self._xmin, self._ymin, self._tmin, self._xmax, self._ymax, self._tmax)
			elif self._xmin is not None and self._zmin is None and self._tmin is None:
				return "'STBOX ((%s, %s), (%s, %s))'" % \
					   (self._xmin, self._ymin, self._xmax, self._ymax)
			elif self._xmin is None and self._zmin is None and self._tmin is not None:
				return "'STBOX T((, %s), (, %s))'" % (self._tmin, self._tmax)
			else:
				raise Exception("ERROR: Wrong values")

	def __repr__(self):
		return (f'{self.__class__.__name__ }'
				f'({self._xmin!r}, {self._ymin!r}, {self._zmin!r}, {self._tmin!r}, '
				f'{self._xmax!r}, {self._ymax!r}, {self._zmax!r}, {self._tmax!r}, {self._geodetic!r})')
