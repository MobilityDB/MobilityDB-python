import pytest
from dateutil.parser import parse
from mobilitydb.main import TBoolInst, TBoolI, TBoolSeq, TBoolS

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tboolinst', [
	'true@2019-09-01 00:00:00+01',
	('true', '2019-09-08 00:00:00+01'),
	['true', '2019-09-08 00:00:00+01'],
	(True, '2019-09-08 00:00:00+01'),
	[True, parse('2019-09-08 00:00:00+01')],
])
async def test_tboolinst_constructors(connection, expected_tboolinst):
	params = TBoolInst(expected_tboolinst)
	await connection.execute('INSERT INTO tbl_tboolinst (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tboolinst WHERE temp=$1', params, column=0)
	assert result == TBoolInst(expected_tboolinst)

@pytest.mark.parametrize('expected_tbooli', [
	'{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
	('true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'),
	(TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	 TBoolInst('true@2019-09-03 00:00:00+01')),
	['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'],
	[TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	 TBoolInst('true@2019-09-03 00:00:00+01')],
])
async def test_tbooli_constructor(connection, expected_tbooli):
	if isinstance(expected_tbooli, tuple):
		params = TBoolI(*expected_tbooli)
	else:
		params = TBoolI(expected_tbooli)
	await connection.execute('INSERT INTO tbl_tbooli (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tbooli WHERE temp=$1', params)
	if isinstance(expected_tbooli, tuple):
		assert result == TBoolI(*expected_tbooli)
	else:
		assert result == TBoolI(expected_tbooli)

@pytest.mark.parametrize('expected_tboolseq', [
	'[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]',
	['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'false@2019-09-03 00:00:00+01'],
	[TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	 TBoolInst('false@2019-09-03 00:00:00+01')],
])
async def test_tboolseq_constructor(connection, expected_tboolseq):
	if isinstance(expected_tboolseq, tuple):
		params = TBoolSeq(*expected_tboolseq)
	else:
		params = TBoolSeq(expected_tboolseq)
	await connection.execute('INSERT INTO tbl_tboolseq (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tboolseq WHERE temp=$1', params)
	if isinstance(expected_tboolseq, tuple):
		assert result == TBoolSeq(*expected_tboolseq)
	else:
		assert result == TBoolSeq(expected_tboolseq)

@pytest.mark.parametrize('expected_tbools', [
	'{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
	['[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'],
	[TBoolSeq('[true@2019-09-01 00:00:00+01]'),
	 TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')],
])
async def test_tbools_constructor(connection, expected_tbools):
	if isinstance(expected_tbools, tuple):
		params = TBoolS(*expected_tbools)
	else:
		params = TBoolS(expected_tbools)
	await connection.execute('INSERT INTO tbl_tbools (temp) VALUES ($1)', params)
	result = await connection.fetchval('SELECT temp FROM tbl_tbools WHERE temp=$1', params)
	if isinstance(expected_tbools, tuple):
		assert result == TBoolS(*expected_tbools)
	else:
		assert result == TBoolS(expected_tbools)
