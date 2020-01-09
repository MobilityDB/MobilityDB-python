import pytest
from dateutil.parser import parse
from postgis import Point
from mobilitydb.main import TGeomPointInst, TGeomPointI, TGeomPointSeq, TGeomPointS

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tgeompointinst', [
	'POINT(10.0 10.0)@2019-09-01 00:00:00+01',
	'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
	('POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
	['POINT(10.0 10.0)', '2019-09-08 00:00:00+01'],
	('SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
	['SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'],
	(Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')),
	[Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')],
	(Point(10.0, 10.0, srid=4326), parse('2019-09-08 00:00:00+01')),
	[Point(10.0, 10.0, srid=4326), parse('2019-09-08 00:00:00+01')],
])
async def test_tgeompointinst_constructors(connection, expected_tgeompointinst):
	params = TGeomPointInst(expected_tgeompointinst)
	await connection.execute('INSERT INTO tbl_tgeompointinst (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tgeompointinst WHERE temp=$1', params, column=0)
	assert result == TGeomPointInst(expected_tgeompointinst)

@pytest.mark.parametrize('expected_tgeompointi', [
	'{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
		'Point(10.0 10.0)@2019-09-03 00:00:00+01}',
	'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
		'Point(10.0 10.0)@2019-09-03 00:00:00+01}',
	('Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'Point(10.0 10.0)@2019-09-03 00:00:00+01'),
	['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'Point(10.0 10.0)@2019-09-03 00:00:00+01'],
	('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'),
	['SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'],
	(TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')),
	[TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
	(TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')),
	[TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
])
async def test_tgeompointi_constructor(connection, expected_tgeompointi):
	if isinstance(expected_tgeompointi, tuple):
		params = TGeomPointI(*expected_tgeompointi)
	else:
		params = TGeomPointI(expected_tgeompointi)
	await connection.execute('INSERT INTO tbl_tgeompointi (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tgeompointi WHERE temp=$1', params)
	if isinstance(expected_tgeompointi, tuple):
		assert result == TGeomPointI(*expected_tgeompointi)
	else:
		assert result == TGeomPointI(expected_tgeompointi)

@pytest.mark.parametrize('expected_tgeompointseq', [
	'[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
		'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
	'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
		'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
	'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
		'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
	'SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
		'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
	['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'Point(10.0 10.0)@2019-09-03 00:00:00+01'],
	['SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'],
	[TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
	[TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
	(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise'),
	(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Linear', 4326),
	(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
		'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise', 4326),
	([TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
	([TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
		TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
])
async def test_tgeompointseq_constructor(connection, expected_tgeompointseq):
	if isinstance(expected_tgeompointseq, tuple):
		params = TGeomPointSeq(*expected_tgeompointseq)
	else:
		params = TGeomPointSeq(expected_tgeompointseq)
	await connection.execute('INSERT INTO tbl_tgeompointseq (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tgeompointseq WHERE temp=$1', params)
	if isinstance(expected_tgeompointseq, tuple):
		assert result == TGeomPointSeq(*expected_tgeompointseq)
	else:
		assert result == TGeomPointSeq(expected_tgeompointseq)

@pytest.mark.parametrize('expected_tgeompoints', [
	'{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
	'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
	'Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
	'SRID=4326;Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
	['[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
	['SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
	(['[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear'),
	(['[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear', 4326),
	(['SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear'),
	(['SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear', 4326),
	(['Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
		'Stepwise'),
	(['SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'SRID=4326;Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
		'Stepwise', 4326),
	(['Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
		'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
		'Stepwise', 4326),
	[TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
		TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
	([TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
		TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Linear'),
	([TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
		TGeomPointSeq(
			'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
	 'Stepwise'),
])
async def test_tgeompoints_constructor(connection, expected_tgeompoints):
	if isinstance(expected_tgeompoints, tuple):
		params = TGeomPointS(*expected_tgeompoints)
	else:
		params = TGeomPointS(expected_tgeompoints)
	await connection.execute('INSERT INTO tbl_tgeompoints (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tgeompoints WHERE temp=$1', params)
	if isinstance(expected_tgeompoints, tuple):
		assert result == TGeomPointS(*expected_tgeompoints)
	else:
		assert result == TGeomPointS(expected_tgeompoints)
