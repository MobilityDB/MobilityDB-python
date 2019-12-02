from dateutil.parser import parse
import re
import warnings

try:
	# Do not make psycopg2 a requirement.
	from psycopg2.extensions import ISQLQuote
except ImportError:
	warnings.warn('psycopg2 not installed', ImportWarning)


class TBox:
	__slots__ = ['xmin', 'tmin', 'xmax', 'tmax']

	def __init__(self, *args):
		try:
			if len(args) == 1 and isinstance(args[0], str):
				self.parseFromString(args[0])
			elif len(args) == 2:
				try:
					self.xmin = float(args[0])
					self.xmax = float(args[1])
					self.tmin = None
					self.tmax = None
				except:
					self.xmin = None
					self.xmax = None
					self.tmin = parse(args[0])
					self.tmax = parse(args[1])
			elif len(args) == 4:
				self.xmin = float(args[0])
				self.tmin = parse(args[1])
				self.xmax = float(args[2])
				self.tmax = parse(args[3])
		except:
			raise Exception("ERROR: Wrong parameters")

	def parseFromString(self, value):
		values = value.replace("TBOX", '')
		if 'T' in values:
			time = True
			self.xmin = None
			self.xmax = None
		else:
			time = False
		values = values.replace('T', '').replace('(', '').replace(')', '').split(',')
		if time:
			self.tmin = parse(values[0])
			self.tmax = parse(values[1])
		elif len(values) == 4:
			self.xmin = float(values[0]) if values[0] != '' and not values[0].isspace() else None
			self.xmax = float(values[2]) if values[2] != '' and not values[2].isspace() else None
			self.tmin = parse(values[1]) if values[1] != '' and not values[1].isspace() else None
			self.tmax = parse(values[3]) if values[3] != '' and not values[3].isspace() else None
		else:
			raise Exception("ERROR: Wrong parameters")

	@staticmethod
	def read_from_cursor(value, cursor=None):
		if not value:
			return None
		return TBOX(value)

	# Psycopg2 interface.
	def __conform__(self, protocol):
		if protocol is ISQLQuote:
			return self

	def getquoted(self):
		return "{}".format(self.__str__())
	# End Psycopg2 interface.

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			# I need to add the other values in the comparison but there is a problem appears when I run the test file
			return self.xmin == other.xmin and self.tmin == other.tmin and self.xmax == other.xmax and self.tmax == other.tmax
		else:
			return False

	def __str__(self):
		if self.xmin is not None and self.tmin is not None:
			return "'TBOX((%s, %s), (%s, %s))'" % (repr(self.xmin), self.tmin, repr(self.xmax), self.tmax)
		elif self.xmin is not None:
			return "'TBOX((%s, ), (%s, ))'" % (repr(self.xmin), repr(self.xmax))
		elif self.tmin is not None:
			return "'TBOX((, %s), (, %s))'" % (self.tmin, self.tmax)

	def __repr__(self):
		if self.xmin is not None and self.tmin is not None:
			return "'TBOX((%s, %s), (%s, %s))'" % (repr(self.xmin), repr(self.tmin), repr(self.xmax), repr(self.tmax))
		elif self.xmin is not None:
			return "'TBOX((%s, ), (%s, ))'" % (repr(self.xmin), repr(self.xmax))
		elif self.tmin is not None:
			return "'TBOX((, %s), (, %s))'" % (repr(self.tmin), repr(self.tmax))
