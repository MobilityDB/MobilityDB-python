import pytest
from datetime import timedelta
from dateutil.parser import parse
from postgis import Point, MultiPoint, LineString, MultiLineString, GeometryCollection
from mobilitydb.main import TGeomPointInst, TGeomPointI, TGeomPointSeq, TGeomPointS
from mobilitydb.main.tpoint import to_coords
from mobilitydb.time import TimestampSet, Period, PeriodSet

from pymeos import GeomPoint
from pymeos.range import RangeGeom
from pymeos.temporal import TemporalDuration


@pytest.mark.parametrize('expected_tgeompointinst', [
    'POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    ('POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    ('SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    (GeomPoint(10.0, 10.0), parse('2019-09-08 00:00:00+01')),
    (GeomPoint(10.0, 10.0, 4326), parse('2019-09-08 00:00:00+01')),
])
def test_tgeompointinst_constructors(cursor, expected_tgeompointinst):
    if isinstance(expected_tgeompointinst, tuple):
        params = [TGeomPointInst(*expected_tgeompointinst)]
    else:
        params = [TGeomPointInst(expected_tgeompointinst)]
    cursor.execute('INSERT INTO tbl_tgeompointinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeompointinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeompointinst, tuple):
        assert result == TGeomPointInst(*expected_tgeompointinst)
    else:
        assert result == TGeomPointInst(expected_tgeompointinst)


@pytest.mark.parametrize('expected_tgeompointinst', [
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
])
def test_tgeompointinst_accessors(cursor, expected_tgeompointinst):
    assert TGeomPointInst(expected_tgeompointinst).srid == 4326
    assert TGeomPointInst(expected_tgeompointinst).duration == TemporalDuration.Instant
    assert TGeomPointInst(expected_tgeompointinst).duration.name == 'Instant'
    assert TGeomPointInst(expected_tgeompointinst).getValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointInst(expected_tgeompointinst).getValues == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointInst(expected_tgeompointinst).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointInst(expected_tgeompointinst).endValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointInst(expected_tgeompointinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TGeomPointInst(expected_tgeompointinst).timespan == timedelta(0)
    assert TGeomPointInst(expected_tgeompointinst).period == Period(
        '[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TGeomPointInst(expected_tgeompointinst).numInstants == 1
    assert TGeomPointInst(expected_tgeompointinst).startInstant == TGeomPointInst(
        'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).endInstant == TGeomPointInst(
        'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).instantN(0) == TGeomPointInst(
        'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).instants == {
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')}
    assert TGeomPointInst(expected_tgeompointinst).numTimestamps == 1
    assert TGeomPointInst(expected_tgeompointinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).timestampN(0) == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).timestamps == {parse('2019-09-01 00:00:00+01')}
    assert TGeomPointInst(expected_tgeompointinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeomPointInst(expected_tgeompointinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
    assert TGeomPointInst(expected_tgeompointinst).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeomPointInst(expected_tgeompointinst).intersectsTimestampSet(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TGeomPointInst(expected_tgeompointinst).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeomPointInst(expected_tgeompointinst).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TGeomPointInst(expected_tgeompointinst).intersectsPeriod(
        Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TGeomPointInst(expected_tgeompointinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeomPointInst(expected_tgeompointinst).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TGeomPointInst(expected_tgeompointinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tgeompointi', [
    '{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01}',
    'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01}',
    {'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'},
    {'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'},
    {TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')},
    {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')},
])
def test_tgeompointi_constructor(cursor, expected_tgeompointi):
    if isinstance(expected_tgeompointi, tuple):
        params = [TGeomPointI(*expected_tgeompointi)]
    else:
        params = [TGeomPointI(expected_tgeompointi)]
    cursor.execute('INSERT INTO tbl_tgeompointi (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeompointi WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeompointi, tuple):
        assert result == TGeomPointI(*expected_tgeompointi)
    else:
        assert result == TGeomPointI(expected_tgeompointi)


@pytest.mark.parametrize('expected_tgeompointi', [
    'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(30.0 30.0)@2019-09-03 00:00:00+01}',
])
def test_tgeompointi_accessors(cursor, expected_tgeompointi):
    assert TGeomPointI(expected_tgeompointi).srid == 4326
    assert TGeomPointI(expected_tgeompointi).duration == TemporalDuration.InstantSet
    assert TGeomPointI(expected_tgeompointi).duration.name == 'InstantSet'
    assert TGeomPointI(expected_tgeompointi).getValues == \
           MultiPoint([Point(10.0, 10.0),Point(20.0, 20.0),Point(30.0, 30.0)])
    assert TGeomPointI(expected_tgeompointi).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointI(expected_tgeompointi).endValue == GeomPoint(30.0, 30.0, 4326)
    assert TGeomPointI(expected_tgeompointi).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointI(expected_tgeompointi).timespan == timedelta(0)
    assert TGeomPointI(expected_tgeompointi).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointI(expected_tgeompointi).numInstants == 3
    assert TGeomPointI(expected_tgeompointi).startInstant == TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointI(expected_tgeompointi).endInstant == TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeomPointI(expected_tgeompointi).instantN(1) == TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointI(expected_tgeompointi).instants == {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                            TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                            TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeomPointI(expected_tgeompointi).numTimestamps == 3
    assert TGeomPointI(expected_tgeompointi).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointI(expected_tgeompointi).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointI(expected_tgeompointi).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointI(expected_tgeompointi).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                              parse('2019-09-02 00:00:00+01'),
                                                              parse('2019-09-03 00:00:00+01')}
    assert TGeomPointI(expected_tgeompointi).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeomPointI(expected_tgeompointi).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeomPointI(expected_tgeompointi).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeomPointI(expected_tgeompointi).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeomPointI(expected_tgeompointi).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeomPointI(expected_tgeompointi).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TGeomPointI(expected_tgeompointi).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeomPointI(expected_tgeompointi).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeomPointI(expected_tgeompointi).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TGeomPointI(expected_tgeompointi).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tgeompointseq', [
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
    {TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')},
    {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')},
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, None, 'Stepwise'),
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 4326, 'Linear'),
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 4326, 'Stepwise'),
    ({TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, None, 'Stepwise'),
    ({TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, None, 'Stepwise'),
])
def test_tgeompointseq_constructor(cursor, expected_tgeompointseq):
    if isinstance(expected_tgeompointseq, tuple):
        params = [TGeomPointSeq(*expected_tgeompointseq)]
    else:
        params = [TGeomPointSeq(expected_tgeompointseq)]
    cursor.execute('INSERT INTO tbl_tgeompointseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeompointseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeompointseq, tuple):
        assert result == TGeomPointSeq(*expected_tgeompointseq)
    else:
        assert result == TGeomPointSeq(expected_tgeompointseq)

@pytest.mark.parametrize('expected_tgeompointseq', [
    'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
    'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
])
def test_tgeompointseq_accessors(cursor, expected_tgeompointseq):
    assert TGeomPointSeq(expected_tgeompointseq).srid == 4326
    assert TGeomPointSeq(expected_tgeompointseq).duration == TemporalDuration.Sequence
    assert TGeomPointSeq(expected_tgeompointseq).duration.name == 'Sequence'
    assert TGeomPointSeq(expected_tgeompointseq).getValues == LineString([Point(10.0, 10.0),Point(20.0, 20.0),Point(10.0, 10.0)])
    assert TGeomPointSeq(expected_tgeompointseq).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointSeq(expected_tgeompointseq).endValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointSeq(expected_tgeompointseq).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointSeq(expected_tgeompointseq).timespan == timedelta(2)
    assert TGeomPointSeq(expected_tgeompointseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointSeq(expected_tgeompointseq).numInstants == 3
    assert TGeomPointSeq(expected_tgeompointseq).startInstant == TGeomPointInst(
        'SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).endInstant == TGeomPointInst(
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).instantN(1) == TGeomPointInst(
        'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).instants == \
           {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
            TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
            TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')}
    assert TGeomPointSeq(expected_tgeompointseq).numTimestamps == 3
    assert TGeomPointSeq(expected_tgeompointseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                                  parse('2019-09-02 00:00:00+01'),
                                                                  parse('2019-09-03 00:00:00+01')}
    assert TGeomPointSeq(expected_tgeompointseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeomPointSeq(expected_tgeompointseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeomPointSeq(expected_tgeompointseq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeomPointSeq(expected_tgeompointseq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeomPointSeq(expected_tgeompointseq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeomPointSeq(expected_tgeompointseq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeomPointSeq(expected_tgeompointseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeomPointSeq(expected_tgeompointseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tgeompoints', [
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
    {TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')},
    ({TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None, 'Linear'),
    ({TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq(
            'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None,
     'Stepwise'),
])
def test_tgeompoints_constructor(cursor, expected_tgeompoints):
    if isinstance(expected_tgeompoints, tuple):
        params = [TGeomPointS(*expected_tgeompoints)]
    else:
        params = [TGeomPointS(expected_tgeompoints)]
    cursor.execute('INSERT INTO tbl_tgeompoints (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeompoints WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeompoints, tuple):
        assert result == TGeomPointS(*expected_tgeompoints)
    else:
        assert result == TGeomPointS(expected_tgeompoints)

@pytest.mark.parametrize('expected_tgeompoints', [
    'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01],  '
    '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]}',
])
def test_tgeompoints_accessors(cursor, expected_tgeompoints):
    assert TGeomPointS(expected_tgeompoints).srid == 4326
    assert TGeomPointS(expected_tgeompoints).duration == TemporalDuration.SequenceSet
    assert TGeomPointS(expected_tgeompoints).duration.name == 'SequenceSet'
    assert TGeomPointS(expected_tgeompoints).getValues == \
        GeometryCollection([Point(10.0, 10.0), LineString([Point(20.0, 20.0), Point(30.0, 30.0)])])
    assert TGeomPointS(expected_tgeompoints).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointS(expected_tgeompoints).endValue == GeomPoint(30.0, 30.0, 4326)
    assert TGeomPointS(expected_tgeompoints).valueRange == RangeGeom(GeomPoint(10.0, 10.0, 4326), GeomPoint(30.0, 30.0, 4326), upper_inc=True)
    assert TGeomPointS(expected_tgeompoints).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointS(expected_tgeompoints).timespan == timedelta(1)
    assert TGeomPointS(expected_tgeompoints).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointS(expected_tgeompoints).numInstants == 3
    assert TGeomPointS(expected_tgeompoints).startInstant == TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointS(expected_tgeompoints).endInstant == TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeomPointS(expected_tgeompoints).instantN(1) == TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointS(expected_tgeompoints).instants == {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                        TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeomPointS(expected_tgeompoints).numTimestamps == 3
    assert TGeomPointS(expected_tgeompoints).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointS(expected_tgeompoints).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointS(expected_tgeompoints).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointS(expected_tgeompoints).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')}
    assert TGeomPointS(expected_tgeompoints).numSequences == 2
    assert TGeomPointS(expected_tgeompoints).startSequence == TGeomPointSeq('SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]')
    assert TGeomPointS(expected_tgeompoints).endSequence == TGeomPointSeq(
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeomPointS(expected_tgeompoints).sequenceN(1) == TGeomPointSeq(
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeomPointS(expected_tgeompoints).sequences == {TGeomPointSeq('SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')}
    assert TGeomPointS(expected_tgeompoints).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeomPointS(expected_tgeompoints).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeomPointS(expected_tgeompoints).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeomPointS(expected_tgeompoints).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeomPointS(expected_tgeompoints).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeomPointS(expected_tgeompoints).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeomPointS(expected_tgeompoints).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeomPointS(expected_tgeompoints).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
