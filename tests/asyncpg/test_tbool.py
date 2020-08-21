import pytest
from dateutil.parser import parse
from mobilitydb.main import TBoolInst, TBoolInstSet, TBoolSeq, TBoolSeqSet

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

@pytest.mark.parametrize('expected_tboolinstset', [
    '{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
    ('true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'),
    (TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('true@2019-09-03 00:00:00+01')),
    ['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'],
    [TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('true@2019-09-03 00:00:00+01')],
])
async def test_tboolinstset_constructor(connection, expected_tboolinstset):
    if isinstance(expected_tboolinstset, tuple):
        params = TBoolInstSet(*expected_tboolinstset)
    else:
        params = TBoolInstSet(expected_tboolinstset)
    await connection.execute('INSERT INTO tbl_tboolinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tboolinstset WHERE temp=$1', params)
    if isinstance(expected_tboolinstset, tuple):
        assert result == TBoolInstSet(*expected_tboolinstset)
    else:
        assert result == TBoolInstSet(expected_tboolinstset)

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

@pytest.mark.parametrize('expected_tboolseqset', [
    '{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
    ['[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'],
    [TBoolSeq('[true@2019-09-01 00:00:00+01]'),
     TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')],
])
async def test_tboolseqset_constructor(connection, expected_tboolseqset):
    if isinstance(expected_tboolseqset, tuple):
        params = TBoolSeqSet(*expected_tboolseqset)
    else:
        params = TBoolSeqSet(expected_tboolseqset)
    await connection.execute('INSERT INTO tbl_tboolseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tboolseqset WHERE temp=$1', params)
    if isinstance(expected_tboolseqset, tuple):
        assert result == TBoolSeqSet(*expected_tboolseqset)
    else:
        assert result == TBoolSeqSet(expected_tboolseqset)
