import pytest
from datetime import timedelta
from dateutil.parser import parse
from postgis import Point, MultiPoint, LineString, MultiLineString, GeometryCollection
from mobilitydb.main import TGeogPointInst, TGeogPointI, TGeogPointSeq, TGeogPointS
from mobilitydb.main.tpoint import to_coords
from mobilitydb.time import TimestampSet, Period, PeriodSet

from pymeos import Geometry as MEOSPoint
from pymeos.temporal import TemporalDuration
from pymeos.temporal import TInstantGeom


@pytest.mark.parametrize('expected_tgeogpointinst', [
    'POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    ('POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    ('SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    (Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')),
    (Point(10.0, 10.0, srid=4326), parse('2019-09-08 00:00:00+01')),
])
def test_tgeogpointinst_constructors(cursor, expected_tgeogpointinst):
    if isinstance(expected_tgeogpointinst, tuple):
        params = [TGeogPointInst(*expected_tgeogpointinst)]
    else:
        params = [TGeogPointInst(expected_tgeogpointinst)]
    cursor.execute('INSERT INTO tbl_tgeogpointinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeogpointinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeogpointinst, tuple):
        assert result == TGeogPointInst(*expected_tgeogpointinst)
    else:
        assert result == TGeogPointInst(expected_tgeogpointinst)


@pytest.mark.parametrize('expected_tgeogpointinst', [
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
])
def test_tgeogpointinst_accessors(cursor, expected_tgeogpointinst):
    # assert TGeogPointInst(expected_tgeogpointinst).srid == 4326
    assert TGeogPointInst(expected_tgeogpointinst).duration == TemporalDuration.Instant
    assert TGeogPointInst(expected_tgeogpointinst).duration.name == 'Instant'
    assert TGeogPointInst(expected_tgeogpointinst).getValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointInst(expected_tgeogpointinst).getValues == MEOSPoint(10.0, 10.0)
    assert TGeogPointInst(expected_tgeogpointinst).startValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointInst(expected_tgeogpointinst).endValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointInst(expected_tgeogpointinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TGeogPointInst(expected_tgeogpointinst).timespan == timedelta(0)
    assert TGeogPointInst(expected_tgeogpointinst).period == Period(
        '[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TGeogPointInst(expected_tgeogpointinst).numInstants == 1
    assert TGeogPointInst(expected_tgeogpointinst).startInstant == TInstantGeom(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).endInstant == TInstantGeom(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).instantN(0) == TInstantGeom(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).instants == {
        TInstantGeom('Point(10.0 10.0)@2019-09-01 00:00:00+01')}
    assert TGeogPointInst(expected_tgeogpointinst).numTimestamps == 1
    assert TGeogPointInst(expected_tgeogpointinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).timestampN(0) == parse('2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).timestamps == {parse('2019-09-01 00:00:00+01')}
    assert TGeogPointInst(expected_tgeogpointinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeogPointInst(expected_tgeogpointinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
    assert TGeogPointInst(expected_tgeogpointinst).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeogPointInst(expected_tgeogpointinst).intersectsTimestampSet(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TGeogPointInst(expected_tgeogpointinst).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeogPointInst(expected_tgeogpointinst).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TGeogPointInst(expected_tgeogpointinst).intersectsPeriod(
        Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TGeogPointInst(expected_tgeogpointinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeogPointInst(expected_tgeogpointinst).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TGeogPointInst(expected_tgeogpointinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False


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
def test_tgeogpointi_constructor(cursor, expected_tgeogpointi):
    if isinstance(expected_tgeogpointi, tuple):
        params = [TGeogPointI(*expected_tgeogpointi)]
    else:
        params = [TGeogPointI(expected_tgeogpointi)]
    cursor.execute('INSERT INTO tbl_tgeogpointi (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeogpointi WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeogpointi, tuple):
        assert result == TGeogPointI(*expected_tgeogpointi)
    else:
        assert result == TGeogPointI(expected_tgeogpointi)


@pytest.mark.parametrize('expected_tgeogpointi', [
    'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(30.0 30.0)@2019-09-03 00:00:00+01}',
])
def test_tgeogpointi_accessors(cursor, expected_tgeogpointi):
    # assert TGeogPointI(expected_tgeogpointi).srid == 4326
    assert TGeogPointI(expected_tgeogpointi).duration == TemporalDuration.InstantSet
    assert TGeogPointI(expected_tgeogpointi).duration.name == 'InstantSet'
    assert TGeogPointI(expected_tgeogpointi).getValues == \
           MultiPoint([Point(10.0, 10.0),Point(20.0, 20.0),Point(30.0, 30.0)])
    assert TGeogPointI(expected_tgeogpointi).startValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointI(expected_tgeogpointi).endValue == MEOSPoint(30.0, 30.0)
    assert TGeogPointI(expected_tgeogpointi).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeogPointI(expected_tgeogpointi).timespan == timedelta(0)
    assert TGeogPointI(expected_tgeogpointi).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeogPointI(expected_tgeogpointi).numInstants == 3
    assert TGeogPointI(expected_tgeogpointi).startInstant == TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointI(expected_tgeogpointi).endInstant == TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeogPointI(expected_tgeogpointi).instantN(1) == TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeogPointI(expected_tgeogpointi).instants == {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                            TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                            TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeogPointI(expected_tgeogpointi).numTimestamps == 3
    assert TGeogPointI(expected_tgeogpointi).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointI(expected_tgeogpointi).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeogPointI(expected_tgeogpointi).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeogPointI(expected_tgeogpointi).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                              parse('2019-09-02 00:00:00+01'),
                                                              parse('2019-09-03 00:00:00+01')}
    assert TGeogPointI(expected_tgeogpointi).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeogPointI(expected_tgeogpointi).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeogPointI(expected_tgeogpointi).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeogPointI(expected_tgeogpointi).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeogPointI(expected_tgeogpointi).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeogPointI(expected_tgeogpointi).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TGeogPointI(expected_tgeogpointi).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeogPointI(expected_tgeogpointi).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeogPointI(expected_tgeogpointi).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TGeogPointI(expected_tgeogpointi).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


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
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 'Stepwise'),
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 'Linear', 4326),
    ({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, 'Stepwise', 4326),
    ({TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, 'Stepwise'),
    ({TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeogPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, 'Stepwise'),
])
def test_tgeogpointseq_constructor(cursor, expected_tgeogpointseq):
    if isinstance(expected_tgeogpointseq, tuple):
        params = [TGeogPointSeq(*expected_tgeogpointseq)]
    else:
        params = [TGeogPointSeq(expected_tgeogpointseq)]
    cursor.execute('INSERT INTO tbl_tgeogpointseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeogpointseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeogpointseq, tuple):
        assert result == TGeogPointSeq(*expected_tgeogpointseq)
    else:
        assert result == TGeogPointSeq(expected_tgeogpointseq)

@pytest.mark.parametrize('expected_tgeogpointseq', [
    'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
    'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
])
def test_tgeogpointseq_accessors(cursor, expected_tgeogpointseq):
    # assert TGeogPointSeq(expected_tgeogpointseq).srid == 4326
    assert TGeogPointSeq(expected_tgeogpointseq).duration == TemporalDuration.Sequence
    assert TGeogPointSeq(expected_tgeogpointseq).duration.name == 'Sequence'
    assert TGeogPointSeq(expected_tgeogpointseq).getValues == LineString([Point(10.0, 10.0),Point(20.0, 20.0),Point(10.0, 10.0)])
    assert TGeogPointSeq(expected_tgeogpointseq).startValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointSeq(expected_tgeogpointseq).endValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointSeq(expected_tgeogpointseq).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeogPointSeq(expected_tgeogpointseq).timespan == timedelta(2)
    assert TGeogPointSeq(expected_tgeogpointseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeogPointSeq(expected_tgeogpointseq).numInstants == 3
    assert TGeogPointSeq(expected_tgeogpointseq).startInstant == TGeogPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointSeq(expected_tgeogpointseq).endInstant == TGeogPointInst(
        'Point(10.0 10.0)@2019-09-03 00:00:00+01')
    assert TGeogPointSeq(expected_tgeogpointseq).instantN(1) == TGeogPointInst(
        'Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeogPointSeq(expected_tgeogpointseq).instants == \
           {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
            TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
            TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')}
    assert TGeogPointSeq(expected_tgeogpointseq).numTimestamps == 3
    assert TGeogPointSeq(expected_tgeogpointseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointSeq(expected_tgeogpointseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeogPointSeq(expected_tgeogpointseq).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeogPointSeq(expected_tgeogpointseq).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                                  parse('2019-09-02 00:00:00+01'),
                                                                  parse('2019-09-03 00:00:00+01')}
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeogPointSeq(expected_tgeogpointseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


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
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, 'Linear'),
    ({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, 'Linear', 4326),
    ({'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, 'Linear'),
    ({'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, 'Linear', 4326),
    ({'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
        'Stepwise'),
    ({'SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
        'Stepwise', 4326),
    ({'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'},
        'Stepwise', 4326),
    {TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')},
    ({TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, 'Linear'),
    ({TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq(
            'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')},
     'Stepwise'),
])
def test_tgeogpoints_constructor(cursor, expected_tgeogpoints):
    if isinstance(expected_tgeogpoints, tuple):
        params = [TGeogPointS(*expected_tgeogpoints)]
    else:
        params = [TGeogPointS(expected_tgeogpoints)]
    cursor.execute('INSERT INTO tbl_tgeogpoints (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeogpoints WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeogpoints, tuple):
        assert result == TGeogPointS(*expected_tgeogpoints)
    else:
        assert result == TGeogPointS(expected_tgeogpoints)

@pytest.mark.parametrize('expected_tgeogpoints', [
    'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01],  '
    '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]}',
])
def test_tgeogpoints_accessors(cursor, expected_tgeogpoints):
    # assert TGeogPointS(expected_tgeogpoints).srid == 4326
    assert TGeogPointS(expected_tgeogpoints).duration == TemporalDuration.SequenceSet
    assert TGeogPointS(expected_tgeogpoints).duration.name == 'SequenceSet'
    assert TGeogPointS(expected_tgeogpoints).getValues == \
        GeometryCollection([Point(10.0, 10.0), LineString([Point(20.0, 20.0), Point(30.0, 30.0)])])
    assert TGeogPointS(expected_tgeogpoints).startValue == MEOSPoint(10.0, 10.0)
    assert TGeogPointS(expected_tgeogpoints).endValue == MEOSPoint(30.0, 30.0)
    # assert TGeogPointS(expected_tgeogpoints).valueRange == geogpointrange(Point(10.0, 10.0), Point(30.0, 30.0), upper_inc=True)
    assert TGeogPointS(expected_tgeogpoints).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeogPointS(expected_tgeogpoints).timespan == timedelta(1)
    assert TGeogPointS(expected_tgeogpoints).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeogPointS(expected_tgeogpoints).numInstants == 3
    assert TGeogPointS(expected_tgeogpoints).startInstant == TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointS(expected_tgeogpoints).endInstant == TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeogPointS(expected_tgeogpoints).instantN(1) == TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeogPointS(expected_tgeogpoints).instants == {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                        TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeogPointS(expected_tgeogpoints).numTimestamps == 3
    assert TGeogPointS(expected_tgeogpoints).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointS(expected_tgeogpoints).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeogPointS(expected_tgeogpoints).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeogPointS(expected_tgeogpoints).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')}
    assert TGeogPointS(expected_tgeogpoints).numSequences == 2
    assert TGeogPointS(expected_tgeogpoints).startSequence == TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]')
    assert TGeogPointS(expected_tgeogpoints).endSequence == TGeogPointSeq(
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeogPointS(expected_tgeogpoints).sequenceN(1) == TGeogPointSeq(
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeogPointS(expected_tgeogpoints).sequences == {TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')}
    assert TGeogPointS(expected_tgeogpoints).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeogPointS(expected_tgeogpoints).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeogPointS(expected_tgeogpoints).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeogPointS(expected_tgeogpoints).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeogPointS(expected_tgeogpoints).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeogPointS(expected_tgeogpoints).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeogPointS(expected_tgeogpoints).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeogPointS(expected_tgeogpoints).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
