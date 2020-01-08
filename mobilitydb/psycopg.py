from psycopg2 import extensions
from mobilitydb.boxes import TBox, STBox
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TBool, TInt, TFloat, TText, TGeomPoint, TGeogPoint


# Suggestion is to have our own connection method to register our types without asking the user to do this step
"""
class MobilityDB:
	@classmethod
	def connect(cls, host_, database_, user_, password_):
		conn = psycopg2.connect(host=host_, database=database_, user=user_, password=password_)
		register(conn)
		return conn
"""

def register(connection):
	if isinstance(connection, extensions.cursor):
		# Retrocompat.
		cursor = connection
	else:
		cursor = connection.cursor()

	# Add MobilityDB types to PostgreSQL adapter and specify the reader function for each type.
	cursor.execute("SELECT NULL::TimestampSet")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TimestampSet", TimestampSet.read_from_cursor))

	cursor.execute("SELECT NULL::Period")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "Period", Period.read_from_cursor))

	cursor.execute("SELECT NULL::PeriodSet")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "PeriodSet", PeriodSet.read_from_cursor))

	cursor.execute("SELECT NULL::TBOX")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TBOX", TBox.read_from_cursor))

	cursor.execute("SELECT NULL::TBool")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TBool", TBool.read_from_cursor))

	cursor.execute("SELECT NULL::TInt")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TInt", TInt.read_from_cursor))

	cursor.execute("SELECT NULL::TFloat")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TFloat", TFloat.read_from_cursor))

	cursor.execute("SELECT NULL::TText")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TText", TText.read_from_cursor))

	cursor.execute("SELECT NULL::STBOX")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "STBOX", STBox.read_from_cursor))

	cursor.execute("SELECT NULL::TGeomPoint")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TGeomPoint", TGeomPoint.read_from_cursor))

	cursor.execute("SELECT NULL::TGeogPoint")
	oid = cursor.description[0][1]
	extensions.register_type(extensions.new_type((oid,), "TGeogPoint", TGeogPoint.read_from_cursor))
