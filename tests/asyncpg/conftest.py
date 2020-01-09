import asyncpg
import pytest
import os
from mobilitydb import *
from mobilitydb.asyncpg import register


time_types = [TimestampSet, Period, PeriodSet]
box_types = [TBox, STBox]
duration_suffixes = ['Inst', 'I', 'Seq', 'S']
duration_types = ['INSTANT', 'INSTANTSET', 'SEQUENCE', 'SEQUENCESET']
temporal_types = [TBool, TInt, TFloat, TText, TGeomPoint, TGeogPoint]


@pytest.yield_fixture
async def connection():
	conn = await asyncpg.connect(database=os.getenv('PGDATABASE', 'test'))
	await register(conn)
	for time in time_types:
		await conn.execute(
			'CREATE TABLE IF NOT EXISTS tbl_' + time.__name__.lower() +
			'(timetype ' + time.__name__.lower() + ' NOT NULL);')
	for box in box_types:
		await conn.execute(
			'CREATE TABLE IF NOT EXISTS tbl_' + box.__name__.lower() +
			'(box ' + box.__name__.lower() + ' NOT NULL);')
	for ttype in temporal_types:
		for suffix, duration in zip(duration_suffixes, duration_types):
			await conn.execute(
				'CREATE TABLE IF NOT EXISTS tbl_' + ttype.__name__.lower() + suffix +
				'(temp ' + ttype.__name__.lower() + '(' + duration + ') NOT NULL);')
	yield conn
	await conn.close()

"""
def pytest_unconfigure():
	for time in time_types:
		cur.execute(
			'DROP TABLE tbl_' + time.__name__.lower() + ';')
	for box in box_types:
		cur.execute(
			'DROP TABLE tbl_' + box.__name__.lower() + ';')
	for ttype, suffix in zip(temporal_types, duration_suffixes):
		cur.execute('DROP TABLE tbl_' + ttype.__name__.lower() + suffix + ';')


@pytest.fixture
def cursor():
	# Make sure tables are clean.
	for time in time_types:
		cur.execute('TRUNCATE TABLE tbl_' + time.__name__.lower() + ';')
	for box in box_types:
		cur.execute('TRUNCATE TABLE tbl_' + box.__name__.lower() + ';')
	for ttype in temporal_types:
		for suffix in duration_suffixes:
			cur.execute('TRUNCATE TABLE tbl_' + ttype.__name__.lower() + suffix + ';')
	return cur
"""
