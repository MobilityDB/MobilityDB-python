import pytest
from dateutil.parser import parse
from mobilitydb.main import TFloatInst, TFloatInstSet, TFloatSeq, TFloatSeqSet

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

@pytest.mark.parametrize('expected_tfloatinstset', [
    '{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01}',
    ('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
    (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
     TFloatInst('10.0@2019-09-03 00:00:00+01')),
    ['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
    [TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
     TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
async def test_tfloatinstseq_constructor(connection, expected_tfloatinstset):
    if isinstance(expected_tfloatinstset, tuple):
        params = TFloatInstSet(*expected_tfloatinstset)
    else:
        params = TFloatInstSet(expected_tfloatinstset)
    await connection.execute('INSERT INTO tbl_tfloatinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tfloatinstset WHERE temp=$1', params)
    if isinstance(expected_tfloatinstset, tuple):
        assert result == TFloatInstSet(*expected_tfloatinstset)
    else:
        assert result == TFloatInstSet(expected_tfloatinstset)

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
    await connection.execute('INSERT INTO tbl_tfloatseqseteq (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tfloatseqseteq WHERE temp=$1', params)
    if isinstance(expected_tfloatseq, tuple):
        assert result == TFloatSeq(*expected_tfloatseq)
    else:
        assert result == TFloatSeq(expected_tfloatseq)

@pytest.mark.parametrize('expected_tfloatseqset', [
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
async def test_tfloatseqset_constructor(connection, expected_tfloatseqset):
    if isinstance(expected_tfloatseqset, tuple):
        params = TFloatSeqSet(*expected_tfloatseqset)
    else:
        params = TFloatSeqSet(expected_tfloatseqset)
    await connection.execute('INSERT INTO tbl_tfloatseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tfloatseqset WHERE temp=$1', params)
    if isinstance(expected_tfloatseqset, tuple):
        assert result == TFloatSeqSet(*expected_tfloatseqset)
    else:
        assert result == TFloatSeqSet(expected_tfloatseqset)
