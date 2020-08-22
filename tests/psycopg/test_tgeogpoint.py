import pytest
from datetime import timedelta
from dateutil.parser import parse

from postgis import Point, MultiPoint, LineString, MultiLineString, GeometryCollection
from pymeos import GeomPoint
from pymeos.temporal import TemporalDuration
from pymeos.range import RangeGeom

from mobilitydb.main import TGeogPointInst, TGeogPointInstSet, TGeogPointSeq, TGeogPointSeqSet
from mobilitydb.time import TimestampSet, Period, PeriodSet


@pytest.mark.parametrize('expected_tgeogpointinst', [
    'POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    ('POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    ('SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    (GeomPoint(10.0, 10.0), parse('2019-09-08 00:00:00+01')),
    (GeomPoint(10.0, 10.0, 4326), parse('2019-09-08 00:00:00+01')),
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
    assert TGeogPointInst(expected_tgeogpointinst).srid == 4326
    assert TGeogPointInst(expected_tgeogpointinst).duration == TemporalDuration.Instant
    assert TGeogPointInst(expected_tgeogpointinst).duration.name == 'Instant'
    assert TGeogPointInst(expected_tgeogpointinst).getValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointInst(expected_tgeogpointinst).getValues == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointInst(expected_tgeogpointinst).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointInst(expected_tgeogpointinst).endValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointInst(expected_tgeogpointinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointInst(expected_tgeogpointinst).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TGeogPointInst(expected_tgeogpointinst).timespan == timedelta(0)
    assert TGeogPointInst(expected_tgeogpointinst).period == Period(
        '[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TGeogPointInst(expected_tgeogpointinst).numInstants == 1
    assert TGeogPointInst(expected_tgeogpointinst).startInstant == TGeogPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=4326)
    assert TGeogPointInst(expected_tgeogpointinst).endInstant == TGeogPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=4326)
    assert TGeogPointInst(expected_tgeogpointinst).instantN(0) == TGeogPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=4326)
    assert TGeogPointInst(expected_tgeogpointinst).instants == {
        TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=4326)}
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


@pytest.mark.parametrize('expected_tgeogpointinstset', [
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
def test_tgeogpointinstset_constructor(cursor, expected_tgeogpointinstset):
    if isinstance(expected_tgeogpointinstset, tuple):
        params = [TGeogPointInstSet(*expected_tgeogpointinstset)]
    else:
        params = [TGeogPointInstSet(expected_tgeogpointinstset)]
    cursor.execute('INSERT INTO tbl_tgeogpointinstset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeogpointinstset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeogpointinstset, tuple):
        assert result == TGeogPointInstSet(*expected_tgeogpointinstset)
    else:
        assert result == TGeogPointInstSet(expected_tgeogpointinstset)


@pytest.mark.parametrize('expected_tgeogpointinstset', [
    'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(30.0 30.0)@2019-09-03 00:00:00+01}',
])
def test_tgeogpointinstset_accessors(cursor, expected_tgeogpointinstset):
    assert TGeogPointInstSet(expected_tgeogpointinstset).srid == 4326
    assert TGeogPointInstSet(expected_tgeogpointinstset).duration == TemporalDuration.InstantSet
    assert TGeogPointInstSet(expected_tgeogpointinstset).duration.name == 'InstantSet'
    assert TGeogPointInstSet(expected_tgeogpointinstset).getValues == \
           MultiPoint([Point(10.0, 10.0),Point(20.0, 20.0),Point(30.0, 30.0)])
    assert TGeogPointInstSet(expected_tgeogpointinstset).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointInstSet(expected_tgeogpointinstset).endValue == GeomPoint(30.0, 30.0, 4326)
    assert TGeogPointInstSet(expected_tgeogpointinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeogPointInstSet(expected_tgeogpointinstset).timespan == timedelta(0)
    assert TGeogPointInstSet(expected_tgeogpointinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeogPointInstSet(expected_tgeogpointinstset).numInstants == 3
    assert TGeogPointInstSet(expected_tgeogpointinstset).startInstant == TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointInstSet(expected_tgeogpointinstset).endInstant == TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeogPointInstSet(expected_tgeogpointinstset).instantN(1) == TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeogPointInstSet(expected_tgeogpointinstset).instants == {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                            TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                            TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeogPointInstSet(expected_tgeogpointinstset).numTimestamps == 3
    assert TGeogPointInstSet(expected_tgeogpointinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointInstSet(expected_tgeogpointinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeogPointInstSet(expected_tgeogpointinstset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeogPointInstSet(expected_tgeogpointinstset).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                              parse('2019-09-02 00:00:00+01'),
                                                              parse('2019-09-03 00:00:00+01')}
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TGeogPointInstSet(expected_tgeogpointinstset).intersectsPeriodSet(
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
    assert TGeogPointSeq(expected_tgeogpointseq).srid == 4326
    assert TGeogPointSeq(expected_tgeogpointseq).duration == TemporalDuration.Sequence
    assert TGeogPointSeq(expected_tgeogpointseq).duration.name == 'Sequence'
    assert TGeogPointSeq(expected_tgeogpointseq).getValues == LineString([Point(10.0, 10.0),Point(20.0, 20.0),Point(10.0, 10.0)])
    assert TGeogPointSeq(expected_tgeogpointseq).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointSeq(expected_tgeogpointseq).endValue == GeomPoint(10.0, 10.0, 4326)
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


@pytest.mark.parametrize('expected_tgeogpointseqset', [
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
def test_tgeogpointseqset_constructor(cursor, expected_tgeogpointseqset):
    if isinstance(expected_tgeogpointseqset, tuple):
        params = [TGeogPointSeqSet(*expected_tgeogpointseqset)]
    else:
        params = [TGeogPointSeqSet(expected_tgeogpointseqset)]
    cursor.execute('INSERT INTO tbl_tgeogpointseqset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeogpointseqset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeogpointseqset, tuple):
        assert result == TGeogPointSeqSet(*expected_tgeogpointseqset)
    else:
        assert result == TGeogPointSeqSet(expected_tgeogpointseqset)

@pytest.mark.parametrize('expected_tgeogpointseqset', [
    'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01],  '
    '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]}',
])
def test_tgeogpointseqset_accessors(cursor, expected_tgeogpointseqset):
    assert TGeogPointSeqSet(expected_tgeogpointseqset).srid == 4326
    assert TGeogPointSeqSet(expected_tgeogpointseqset).duration == TemporalDuration.SequenceSet
    assert TGeogPointSeqSet(expected_tgeogpointseqset).duration.name == 'SequenceSet'
    assert TGeogPointSeqSet(expected_tgeogpointseqset).getValues == \
        GeometryCollection([Point(10.0, 10.0), LineString([Point(20.0, 20.0), Point(30.0, 30.0)])])
    assert TGeogPointSeqSet(expected_tgeogpointseqset).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeogPointSeqSet(expected_tgeogpointseqset).endValue == GeomPoint(30.0, 30.0, 4326)
    assert TGeogPointSeqSet(expected_tgeogpointseqset).valueRange == RangeGeom(GeomPoint(10.0, 10.0, 4326), GeomPoint(30.0, 30.0, 4326), upper_inc=True)
    assert TGeogPointSeqSet(expected_tgeogpointseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).timespan == timedelta(1)
    assert TGeogPointSeqSet(expected_tgeogpointseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).numInstants == 3
    assert TGeogPointSeqSet(expected_tgeogpointseqset).startInstant == TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).endInstant == TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).instantN(1) == TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).instants == {TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                        TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                        TGeogPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeogPointSeqSet(expected_tgeogpointseqset).numTimestamps == 3
    assert TGeogPointSeqSet(expected_tgeogpointseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')}
    assert TGeogPointSeqSet(expected_tgeogpointseqset).numSequences == 2
    assert TGeogPointSeqSet(expected_tgeogpointseqset).startSequence == TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).endSequence == TGeogPointSeq(
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).sequenceN(1) == TGeogPointSeq(
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeogPointSeqSet(expected_tgeogpointseqset).sequences == {TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')}
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeogPointSeqSet(expected_tgeogpointseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
