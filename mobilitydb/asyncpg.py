import asyncio
import asyncpg
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.boxes import TBox, STBox
from mobilitydb.main import TBool, TInt, TFloat, TText, TGeomPoint, TGeogPoint

# Suggestion is to have our own connection method to register our types without asking the user to do this step
"""
class MobilityDB:
	@classmethod
	async def connect(cls, host_, database_, user_, password_):
		conn = await asyncpg.connect(host=host_, database=database_, user=user_, password=password_)
		register(conn)
		return conn
"""

async def register(conn):
	# Add MobilityDB types to PostgreSQL adapter and specify the encoder and decoder functions for each type.
	await conn.set_type_codec("timestampset", encoder=TimestampSet.write, decoder=TimestampSet.read_from_cursor)
	await conn.set_type_codec("period", encoder=Period.write, decoder=Period.read_from_cursor)
	await conn.set_type_codec("periodset", encoder=PeriodSet.write, decoder=PeriodSet.read_from_cursor)
	await conn.set_type_codec("tbox", encoder=TBox.write, decoder=TBox.read_from_cursor)
	await conn.set_type_codec("tbool", encoder=TBool.write, decoder=TBool.read_from_cursor)
	await conn.set_type_codec("tint", encoder=TInt.write, decoder=TInt.read_from_cursor)
	await conn.set_type_codec("tfloat", encoder=TFloat.write, decoder=TFloat.read_from_cursor)
	await conn.set_type_codec("ttext", encoder=TText.write, decoder=TText.read_from_cursor)
	await conn.set_type_codec("stbox", encoder=STBox.write, decoder=STBox.read_from_cursor)
	await conn.set_type_codec("tgeompoint", encoder=TGeomPoint.write, decoder=TGeomPoint.read_from_cursor)
	await conn.set_type_codec("tgeogpoint", encoder=TGeogPoint.write, decoder=TGeogPoint.read_from_cursor)
