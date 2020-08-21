import pytest
from dateutil.parser import parse
from mobilitydb.main import TTextInst, TTextInstSet, TTextSeq, TTextSeqSet

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
async def test_ttextinstset_constructor(connection, expected_ttextinstset):
    if isinstance(expected_ttextinstset, tuple):
        params = TTextInstSet(*expected_ttextinstset)
    else:
        params = TTextInstSet(expected_ttextinstset)
    await connection.execute('INSERT INTO tbl_ttextinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_ttextinstset WHERE temp=$1', params)
    if isinstance(expected_ttextinstset, tuple):
        assert result == TTextInstSet(*expected_ttextinstset)
    else:
        assert result == TTextInstSet(expected_ttextinstset)

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

@pytest.mark.parametrize('expected_ttextseqset', [
    '{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}',
    ['[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'],
    [TTextSeq('[AA@2019-09-01 00:00:00+01]'),
     TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')],
])
async def test_ttextseqset_constructor(connection, expected_ttextseqset):
    if isinstance(expected_ttextseqset, tuple):
        params = TTextSeqSet(*expected_ttextseqset)
    else:
        params = TTextSeqSet(expected_ttextseqset)
    await connection.execute('INSERT INTO tbl_ttextseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_ttextseqset WHERE temp=$1', params)
    if isinstance(expected_ttextseqset, tuple):
        assert result == TTextSeqSet(*expected_ttextseqset)
    else:
        assert result == TTextSeqSet(expected_ttextseqset)
