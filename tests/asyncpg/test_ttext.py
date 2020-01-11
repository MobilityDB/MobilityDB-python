import pytest
from dateutil.parser import parse
from mobilitydb.main import TTextInst, TTextI, TTextSeq, TTextS

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_ttextinst', [
    'AA@2019-09-01 00:00:00+01',
    ('AA', '2019-09-08 00:00:00+01'),
    ['AA', '2019-09-08 00:00:00+01'],
    ('AA', parse('2019-09-08 00:00:00+01')),
    ['AA', parse('2019-09-08 00:00:00+01')],
])
async def test_ttextinst_constructors(connection, expected_ttextinst):
    params = TTextInst(expected_ttextinst)
    await connection.execute('INSERT INTO tbl_ttextinst (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_ttextinst WHERE temp=$1', params, column=0)
    assert result == TTextInst(expected_ttextinst)

@pytest.mark.parametrize('expected_ttexti', [
    '{AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01}',
    ('AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'),
    (TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('AA@2019-09-03 00:00:00+01')),
    ['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'],
    [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('AA@2019-09-03 00:00:00+01')],
])
async def test_ttexti_constructor(connection, expected_ttexti):
    if isinstance(expected_ttexti, tuple):
        params = TTextI(*expected_ttexti)
    else:
        params = TTextI(expected_ttexti)
    await connection.execute('INSERT INTO tbl_ttexti (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_ttexti WHERE temp=$1', params)
    if isinstance(expected_ttexti, tuple):
        assert result == TTextI(*expected_ttexti)
    else:
        assert result == TTextI(expected_ttexti)

@pytest.mark.parametrize('expected_ttextseq', [
    '[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]',
    ['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'BB@2019-09-03 00:00:00+01'],
    [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('BB@2019-09-03 00:00:00+01')],
])
async def test_ttextseq_constructor(connection, expected_ttextseq):
    if isinstance(expected_ttextseq, tuple):
        params = TTextSeq(*expected_ttextseq)
    else:
        params = TTextSeq(expected_ttextseq)
    await connection.execute('INSERT INTO tbl_ttextseq (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_ttextseq WHERE temp=$1', params)
    if isinstance(expected_ttextseq, tuple):
        assert result == TTextSeq(*expected_ttextseq)
    else:
        assert result == TTextSeq(expected_ttextseq)

@pytest.mark.parametrize('expected_ttexts', [
    '{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}',
    ['[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'],
    [TTextSeq('[AA@2019-09-01 00:00:00+01]'),
     TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')],
])
async def test_ttexts_constructor(connection, expected_ttexts):
    if isinstance(expected_ttexts, tuple):
        params = TTextS(*expected_ttexts)
    else:
        params = TTextS(expected_ttexts)
    await connection.execute('INSERT INTO tbl_ttexts (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_ttexts WHERE temp=$1', params)
    if isinstance(expected_ttexts, tuple):
        assert result == TTextS(*expected_ttexts)
    else:
        assert result == TTextS(expected_ttexts)
