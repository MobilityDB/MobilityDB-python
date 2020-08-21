import pytest
from dateutil.parser import parse
from postgis import Point
from mobilitydb.main import TGeogPointInst, TGeogPointInstSet, TGeogPointSeq, TGeogPointSeqSet

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tgeogpointinst', [
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
async def test_tgeogpointinst_constructors(connection, expected_tgeogpointinst):
    params = TGeogPointInst(expected_tgeogpointinst)
    await connection.execute('INSERT INTO tbl_tgeogpointinst (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeogpointinst WHERE temp=$1', params, column=0)
    assert result == TGeogPointInst(expected_tgeogpointinst)

@pytest.mark.parametrize('expected_tgeogpointi', [
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
    (TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')),
    [TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    (TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')),
    [TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
])
async def test_tgeogpointinstset_constructor(connection, expected_tgeogpointinstset):
    if isinstance(expected_tgeogpointinstset, tuple):
        params = TGeogPointInstSet(*expected_tgeogpointinstset)
    else:
        params = TGeogPointInstSet(expected_tgeogpointinstset)
    await connection.execute('INSERT INTO tbl_tgeogpointinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeogpointinstset WHERE temp=$1', params)
    if isinstance(expected_tgeogpointinstset, tuple):
        assert result == TGeogPointInstSet(*expected_tgeogpointinstset)
    else:
        assert result == TGeogPointInstSet(expected_tgeogpointinstset)

@pytest.mark.parametrize('expected_tgeogpointseq', [
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
    [TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    [TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise'),
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Linear', 4326),
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise', 4326),
    ([TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
    ([TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
])
async def test_tgeogpointseq_constructor(connection, expected_tgeogpointseq):
    if isinstance(expected_tgeogpointseq, tuple):
        params = TGeogPointSeq(*expected_tgeogpointseq)
    else:
        params = TGeogPointSeq(expected_tgeogpointseq)
    await connection.execute('INSERT INTO tbl_tgeogpointseq (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeogpointseq WHERE temp=$1', params)
    if isinstance(expected_tgeogpointseq, tuple):
        assert result == TGeogPointSeq(*expected_tgeogpointseq)
    else:
        assert result == TGeogPointSeq(expected_tgeogpointseq)

@pytest.mark.parametrize('expected_tgeogpointseqset', [
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
    [TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
    ([TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Linear'),
    ([TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq(
            'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
     'Stepwise'),
])
async def test_tgeogpointseqset_constructor(connection, expected_tgeogpointseqset):
    if isinstance(expected_tgeogpointseqset, tuple):
        params = TGeogPointSeqSet(*expected_tgeogpointseqset)
    else:
        params = TGeogPointSeqSet(expected_tgeogpointseqset)
    await connection.execute('INSERT INTO tbl_tgeogpointseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeogpointseqset WHERE temp=$1', params)
    if isinstance(expected_tgeogpointseqset, tuple):
        assert result == TGeogPointSeqSet(*expected_tgeogpointseqset)
    else:
        assert result == TGeogPointSeqSet(expected_tgeogpointseqset)
