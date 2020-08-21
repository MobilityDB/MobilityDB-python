import pytest
from dateutil.parser import parse
from mobilitydb.main import TIntInst, TIntInstSet, TIntSeq, TIntSeqSet

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tintinst', [
    '10@2019-09-01 00:00:00+01',
    ('10', '2019-09-08 00:00:00+01'),
    ['10', '2019-09-08 00:00:00+01'],
    (10, parse('2019-09-08 00:00:00+01')),
    [10, parse('2019-09-08 00:00:00+01')],
])
async def test_tintinst_constructors(connection, expected_tintinst):
    params = TIntInst(expected_tintinst)
    await connection.execute('INSERT INTO tbl_tintinst (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tintinst WHERE temp=$1', params, column=0)
    assert result == TIntInst(expected_tintinst)

@pytest.mark.parametrize('expected_tintinstset', [
    '{10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01}',
    ('10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'),
    (TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')),
    ['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'],
    [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')],
])
async def test_tintinstset_constructor(connection, expected_tintinstset):
    if isinstance(expected_tintinstset, tuple):
        params = TIntInstSet(*expected_tintinstset)
    else:
        params = TIntInstSet(expected_tintinstset)
    await connection.execute('INSERT INTO tbl_tintinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tintinstset WHERE temp=$1', params)
    if isinstance(expected_tintinstset, tuple):
        assert result == TIntInstSet(*expected_tintinstset)
    else:
        assert result == TIntInstSet(expected_tintinstset)

@pytest.mark.parametrize('expected_tintseq', [
    '[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]',
    ['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '20@2019-09-03 00:00:00+01'],
    [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('20@2019-09-03 00:00:00+01')],
])
async def test_tintseq_constructor(connection, expected_tintseq):
    if isinstance(expected_tintseq, tuple):
        params = TIntSeq(*expected_tintseq)
    else:
        params = TIntSeq(expected_tintseq)
    await connection.execute('INSERT INTO tbl_tintseq (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tintseq WHERE temp=$1', params)
    if isinstance(expected_tintseq, tuple):
        assert result == TIntSeq(*expected_tintseq)
    else:
        assert result == TIntSeq(expected_tintseq)

@pytest.mark.parametrize('expected_tintseqset', [
    '{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}',
    ['[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'],
    [TIntSeq('[10@2019-09-01 00:00:00+01]'),
     TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')],
])
async def test_tintseqset_constructor(connection, expected_tintseqset):
    if isinstance(expected_tintseqset, tuple):
        params = TIntSeqSet(*expected_tintseqset)
    else:
        params = TIntSeqSet(expected_tintseqset)
    await connection.execute('INSERT INTO tbl_tintseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tintseqset WHERE temp=$1', params)
    if isinstance(expected_tintseqset, tuple):
        assert result == TIntSeqSet(*expected_tintseqset)
    else:
        assert result == TIntSeqSet(expected_tintseqset)
