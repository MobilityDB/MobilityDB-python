import pytest
from dateutil.parser import parse
from mobilitydb.main import TIntInst, TIntI, TIntSeq, TIntS

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

@pytest.mark.parametrize('expected_tinti', [
    '{10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01}',
    ('10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'),
    (TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')),
    ['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'],
    [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')],
])
async def test_tinti_constructor(connection, expected_tinti):
    if isinstance(expected_tinti, tuple):
        params = TIntI(*expected_tinti)
    else:
        params = TIntI(expected_tinti)
    await connection.execute('INSERT INTO tbl_tinti (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tinti WHERE temp=$1', params)
    if isinstance(expected_tinti, tuple):
        assert result == TIntI(*expected_tinti)
    else:
        assert result == TIntI(expected_tinti)

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

@pytest.mark.parametrize('expected_tints', [
    '{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}',
    ['[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'],
    [TIntSeq('[10@2019-09-01 00:00:00+01]'),
     TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')],
])
async def test_tints_constructor(connection, expected_tints):
    if isinstance(expected_tints, tuple):
        params = TIntS(*expected_tints)
    else:
        params = TIntS(expected_tints)
    await connection.execute('INSERT INTO tbl_tints (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tints WHERE temp=$1', params)
    if isinstance(expected_tints, tuple):
        assert result == TIntS(*expected_tints)
    else:
        assert result == TIntS(expected_tints)
