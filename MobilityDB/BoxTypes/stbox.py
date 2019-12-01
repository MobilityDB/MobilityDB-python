from dateutil.parser import parse
import re
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class STBOX:
	__slots__ = ['xmin', 'ymin', 'zmin', 'tmin', 'xmax', 'ymax', 'zmax', 'tmax', 'geodetic']

	def __init__(self, *args, geodetic=False):
		try:
			if len(args) == 1 and isinstance(args[0], str):
				self.parseFromString(args[0])
			else:
				if len(args) >= 4:
					self.xmin = float(args[0])
					self.xmax = float(args[int(len(args) / 2)])
					self.ymin = float(args[1])
					self.ymax = float(args[1 + int(len(args) / 2)])
					self.tmin = None
					self.tmax = None
				if len(args) >= 6:
					self.zmin = float(args[2])
					self.zmax = float(args[2 + int(len(args) / 2)])
					self.tmin = None
					self.tmax = None
				if len(args) >= 8:
					self.tmin = parse(args[int(len(args) / 2) - 1])
					self.tmax = parse(args[(int(len(args) / 2) - 1) + int(len(args) / 2)])
				if geodetic:
					self.geodetic = geodetic if geodetic is not None else False

		except:
			raise Exception("ERROR: wrong parameters")

	def parseFromString(self, value):
		if isinstance(value, str) and value is not None:
			values = None
			if 'GEODSTBOX' in value:
				self.geodetic = True
				value = value.replace("GEODSTBOX", '')
				if 'T' not in value:
					self.tmin = None
					self.tmax = None
				values = value.replace('T', '').replace('(', '').replace(')', '').split(',')
			elif 'STBOX' in value:
				self.geodetic = False
				value = value.replace("STBOX", '')
				if 'Z' not in value:
					self.zmin = None
					self.zmax = None
				if 'T' not in value:
					self.tmin = None
					self.tmax = None
				values = value.replace('Z', '').replace('T', ''). \
					replace('(', '').replace(')', '').split(',')
			else:
				raise Exception("ERROR: Input must be STBOX")

			if self.xmin is not None:
				self.xmin = float(values[0])
				self.xmax = float(values[int(len(values) / 2)])
				self.ymin = float(values[1])
				self.ymax = float(values[1 + int(len(values) / 2)])
			if self.zmin is not None:
				self.zmin = float(values[2])
				self.zmax = float(values[2 + int(len(values) / 2)])
			if self.tmin is not None:
				self.tmin = format(values[int(len(values) / 2) - 1])
				self.tmax = format(values[(int(len(values) / 2) - 1) + int(len(values) / 2)])
		else:
			raise Exception("ERROR: wrong parameters")

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
		if self.flags & 0x20:
			if self.flags & 0x10:
				return "GEODSTBOX T((%s, %s, %s, '%s'), (%s, %s, %s, %s))" % \
					   (self.xmin, self.ymin, self.zmin, self.tmin, self.xmax, self.ymax, self.zmax, self.tmax)
			else:
				return "GEODSTBOX((%s, %s, %s), (%s, %s, %s))" % \
					   (self.xmin, self.ymin, self.zmin,
																  self.xmax, self.ymax, self.zmax)
		else:
			if self.flags & 0x04 and self.flags & 0x08 and self.flags & 0x10:
				return "STBOX ZT((%s, %s, %s, %s), (%s, %s, %s, %s))" % (self.xmin, self.ymin, self.zmin, self.tmin,
																		 self.xmax, self.ymax, self.zmax, self.tmax)
			elif self.flags & 0x04 and self.flags & 0x08 and not (self.flags & 0x10):
				return "STBOX Z((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.zmin,
																self.xmax, self.ymax, self.zmax)
			elif self.flags & 0x04 and not (self.flags & 0x08) and self.flags & 0x10:
				return "STBOX T((%s, %s, %s), (%s, %s, %s))" % (self.xmin, self.ymin, self.tmin,
																self.xmax, self.ymax, self.tmax)
			elif self.flags & 0x04:
				return "STBOX ((%s, %s), (%s, %s))" % (self.xmin, self.ymin, self.xmax, self.ymax)
			else:
				raise Exception("ERROR: Wrong values")
