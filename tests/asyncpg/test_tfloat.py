import pytest
from dateutil.parser import parse
from mobilitydb.main import TFloatInst, TFloatI, TFloatSeq, TFloatS

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tfloatinst', [
	'10.0@2019-09-01 00:00:00+01',
	('10.0', '2019-09-08 00:00:00+01'),
	['10.0', '2019-09-08 00:00:00+01'],
	(10.0, parse('2019-09-08 00:00:00+01')),
	[10.0, parse('2019-09-08 00:00:00+01')],
])
async def test_tfloatinst_constructors(connection, expected_tfloatinst):
	params = TFloatInst(expected_tfloatinst)
	await connection.execute('INSERT INTO tbl_tfloatinst (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tfloatinst WHERE temp=$1', params, column=0)
	assert result == TFloatInst(expected_tfloatinst)

@pytest.mark.parametrize('expected_tfloati', [
	'{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01}',
	('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
	(TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
	 TFloatInst('10.0@2019-09-03 00:00:00+01')),
	['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
	[TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
	 TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
async def test_tfloati_constructor(connection, expected_tfloati):
	if isinstance(expected_tfloati, tuple):
		params = TFloatI(*expected_tfloati)
	else:
		params = TFloatI(expected_tfloati)
	await connection.execute('INSERT INTO tbl_tfloati (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tfloati WHERE temp=$1', params)
	if isinstance(expected_tfloati, tuple):
		assert result == TFloatI(*expected_tfloati)
	else:
		assert result == TFloatI(expected_tfloati)

@pytest.mark.parametrize('expected_tfloatseq', [
	'[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
	'Interp=Stepwise;[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
	['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
	[TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
	 TFloatInst('10.0@2019-09-03 00:00:00+01')],
	(['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'], True, True,
	 'Stepwise'),
	([TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
	  TFloatInst('10.0@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
])
async def test_tfloatseq_constructor(connection, expected_tfloatseq):
	if isinstance(expected_tfloatseq, tuple):
		params = TFloatSeq(*expected_tfloatseq)
	else:
		params = TFloatSeq(expected_tfloatseq)
	await connection.execute('INSERT INTO tbl_tfloatseq (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tfloatseq WHERE temp=$1', params)
	if isinstance(expected_tfloatseq, tuple):
		assert result == TFloatSeq(*expected_tfloatseq)
	else:
		assert result == TFloatSeq(expected_tfloatseq)

@pytest.mark.parametrize('expected_tfloats', [
	'{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
	'Interp=Stepwise;{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
	['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'],
	(['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'], 'Linear'),
	(['Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]',
	  'Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'], 'Stepwise'),
	[TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
	 TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')],
	([TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
	  TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')], 'Linear'),
	([TFloatSeq('Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]'),
	  TFloatSeq('Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')], 'Stepwise'),
])
async def test_tfloats_constructor(connection, expected_tfloats):
	if isinstance(expected_tfloats, tuple):
		params = TFloatS(*expected_tfloats)
	else:
		params = TFloatS(expected_tfloats)
	await connection.execute('INSERT INTO tbl_tfloats (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tfloats WHERE temp=$1', params)
	if isinstance(expected_tfloats, tuple):
		assert result == TFloatS(*expected_tfloats)
	else:
		assert result == TFloatS(expected_tfloats)
