from dateutil.parser import parse
import re
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class STBox:
	__slots__ = ['xmin', 'ymin', 'zmin', 'tmin', 'xmax', 'ymax', 'zmax', 'tmax', 'geodetic']

	def __init__(self, *args, geodetic=False):
		self.xmin = self.xmax = self.ymin = self.ymax = self.zmin = self.zmax = self.tmin = self.tmax = None
		self.geodetic = geodetic if geodetic is not None else False
		try:
			if len(args) == 1 and isinstance(args[0], str):
				self.parseFromString(args[0])
			elif len(args) == 2:
				self.tmin = parse(args[0])
				self.tmax = parse(args[1])
				self.xmin = self.xmax = self.ymin = self.ymax = self.zmin = self.zmax = None
			else:
				if len(args) >= 4:
					self.xmin = float(args[0])
					self.xmax = float(args[int(len(args) / 2)])
					self.ymin = float(args[1])
					self.ymax = float(args[1 + int(len(args) / 2)])
				if len(args) >= 6:
					try:
						self.zmin = float(args[2])
						self.zmax = float(args[2 + int(len(args) / 2)])
					except:
						self.tmin = parse(args[2])
						self.tmax = parse(args[2 + int(len(args) / 2)])
				if len(args) >= 8:
					self.tmin = parse(args[int(len(args) / 2) - 1])
					self.tmax = parse(args[(int(len(args) / 2) - 1) + int(len(args) / 2)])
		except:
			raise Exception("ERROR: wrong parameters")

	def parseFromString(self, value):
		if value is None or not isinstance(value, str):
			raise Exception("ERROR: wrong parameters")

		values = None
		if 'GEODSTBOX' in value:
			self.geodetic = True
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
			self.tmin = parse(values[0])
			self.tmax = parse(values[1])
		else:
			if len(values) >= 4:
				self.xmin = float(values[0])
				self.xmax = float(values[int(len(values) / 2)])
				self.ymin = float(values[1])
				self.ymax = float(values[1 + int(len(values) / 2)])
			if hasz:
				self.zmin = float(values[2])
				self.zmax = float(values[2 + int(len(values) / 2)])
			if hast:
				self.tmin = parse(values[int(len(values) / 2) - 1])
				self.tmax = parse(values[(int(len(values) / 2) - 1) + int(len(values) / 2)])

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return STBOX(value)

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

	def __str__(self):
		if self.geodetic:
			if self.tmin is not None:
				if self.xmin is not None:
					return "'GEODSTBOX T((%s, %s, %s, %s), (%s, %s, %s, %s))'" % \
						(self.xmin, self.ymin, self.zmin, self.tmin, self.xmax, self.ymax, self.zmax, self.tmax)
				else:
					return "'GEODSTBOX T((, %s), (, %s))'" % (self.tmin, self.tmax)
			else:
				return "'GEODSTBOX((%s, %s, %s), (%s, %s, %s))'" % \
					(self.xmin, self.ymin, self.zmin, self.xmax, self.ymax, self.zmax)
		else:
			if self.xmin is not None and self.zmin is not None and self.tmin is not None:
				return "'STBOX ZT((%s, %s, %s, %s), (%s, %s, %s, %s))'" % \
					(self.xmin, self.ymin, self.zmin, self.tmin, self.xmax, self.ymax, self.zmax, self.tmax)
			elif self.xmin is not None and self.zmin is not None and self.tmin is None:
				return "'STBOX Z((%s, %s, %s), (%s, %s, %s))'" % \
					(self.xmin, self.ymin, self.zmin, self.xmax, self.ymax, self.zmax)
			elif self.xmin is not None and self.zmin is None and self.tmin is not None:
				return "'STBOX T((%s, %s, %s), (%s, %s, %s))'" % \
					(self.xmin, self.ymin, self.tmin, self.xmax, self.ymax, self.tmax)
			elif self.xmin is not None and self.zmin is None and self.tmin is None:
				return "'STBOX ((%s, %s), (%s, %s))'" % \
					   (self.xmin, self.ymin, self.xmax, self.ymax)
			elif self.xmin is None and self.zmin is None and self.tmin is not None:
				return "'STBOX T(, %s), (, %s))'" % (self.tmin, self.tmax)
			else:
				raise Exception("ERROR: Wrong values")
