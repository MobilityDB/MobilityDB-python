import pytest
from dateutil.parser import parse
from mobilitydb.main import TGeogPointInst, TGeogPointI, TGeogPointSeq, TGeogPointS

from pymeos import GeomPoint as Point

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tgeogpointinst', [
    'POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    ('POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    ('SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    (Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')),
    (Point(10.0, 10.0, 4326), parse('2019-09-08 00:00:00+01')),
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
    {'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'},
    {'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'},
    {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')},
    {TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')},
])
async def test_tgeogpointi_constructor(connection, expected_tgeogpointi):
    if isinstance(expected_tgeogpointi, tuple):
        params = TGeogPointI(*expected_tgeogpointi)
    else:
        params = TGeogPointI(expected_tgeogpointi)
    print(params)
    await connection.execute('INSERT INTO tbl_tgeogpointi (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeogpointi WHERE temp=$1', params)
    if isinstance(expected_tgeogpointi, tuple):
        assert result == TGeogPointI(*expected_tgeogpointi)
    else:
        assert result == TGeogPointI(expected_tgeogpointi)

@pytest.mark.parametrize('expected_tgeogpointseq', [
    '[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    'SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    {'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'},
    {'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'},
    {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')},
    {TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')},
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, None, 'Stepwise'),
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 4326, 'Linear'),
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 4326, 'Stepwise'),
    ({TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, None, 'Stepwise'),
    ({TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, None, 'Stepwise'),
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

@pytest.mark.parametrize('expected_tgeogpoints', [
    '{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    'Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    'SRID=4326;Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    {'[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
    {'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
    ({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None, 'Linear'),
    ({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, 4326, 'Linear'),
    ({'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None, 'Linear'),
    ({'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, 4326, 'Linear'),
    ({'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None,
        'Stepwise'),
    ({'SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
        4326, 'Stepwise'),
    ({'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
        4326, 'Stepwise'),
    {TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')},
    ({TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None, 'Linear'),
    ({TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq(
            'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None,
     'Stepwise'),
])
async def test_tgeogpoints_constructor(connection, expected_tgeogpoints):
    if isinstance(expected_tgeogpoints, tuple):
        params = TGeogPointS(*expected_tgeogpoints)
    else:
        params = TGeogPointS(expected_tgeogpoints)
    await connection.execute('INSERT INTO tbl_tgeogpoints (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeogpoints WHERE temp=$1', params)
    if isinstance(expected_tgeogpoints, tuple):
        assert result == TGeogPointS(*expected_tgeogpoints)
    else:
        assert result == TGeogPointS(expected_tgeogpoints)
