from datetime import timedelta
from dateutil.parser import parse

import pytest
from postgis import Point, MultiPoint, LineString, MultiLineString, GeometryCollection
from pymeos import GeomPoint
from pymeos.range import RangeGeom
from pymeos.temporal import TemporalDuration

from mobilitydb.main import TGeomPointInst, TGeomPointInstSet, TGeomPointSeq, TGeomPointSeqSet
from mobilitydb.time import TimestampSet, Period, PeriodSet


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


@pytest.mark.parametrize('expected_tgeompointinstset', [
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
def test_tgeompointinstset_constructor(cursor, expected_tgeompointinstset):
    if isinstance(expected_tgeompointinstset, tuple):
        params = [TGeomPointInstSet(*expected_tgeompointinstset)]
    else:
        params = [TGeomPointInstSet(expected_tgeompointinstset)]
    cursor.execute('INSERT INTO tbl_tgeompointinstset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeompointinstset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeompointinstset, tuple):
        assert result == TGeomPointInstSet(*expected_tgeompointinstset)
    else:
        assert result == TGeomPointInstSet(expected_tgeompointinstset)


@pytest.mark.parametrize('expected_tgeompointinstset', [
    'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(30.0 30.0)@2019-09-03 00:00:00+01}',
])
def test_tgeompointinstset_accessors(cursor, expected_tgeompointinstset):
    assert TGeomPointInstSet(expected_tgeompointinstset).srid == 4326
    assert TGeomPointInstSet(expected_tgeompointinstset).duration == TemporalDuration.InstantSet
    assert TGeomPointInstSet(expected_tgeompointinstset).duration.name == 'InstantSet'
    assert TGeomPointInstSet(expected_tgeompointinstset).getValues == \
           MultiPoint([Point(10.0, 10.0),Point(20.0, 20.0),Point(30.0, 30.0)])
    assert TGeomPointInstSet(expected_tgeompointinstset).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointInstSet(expected_tgeompointinstset).endValue == GeomPoint(30.0, 30.0, 4326)
    assert TGeomPointInstSet(expected_tgeompointinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointInstSet(expected_tgeompointinstset).timespan == timedelta(0)
    assert TGeomPointInstSet(expected_tgeompointinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointInstSet(expected_tgeompointinstset).numInstants == 3
    assert TGeomPointInstSet(expected_tgeompointinstset).startInstant == TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).endInstant == TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).instantN(1) == TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).instants == {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                            TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                            TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeomPointInstSet(expected_tgeompointinstset).numTimestamps == 3
    assert TGeomPointInstSet(expected_tgeompointinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                              parse('2019-09-02 00:00:00+01'),
                                                              parse('2019-09-03 00:00:00+01')}
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TGeomPointInstSet(expected_tgeompointinstset).intersectsPeriodSet(
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


@pytest.mark.parametrize('expected_tgeompointseqset', [
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
def test_tgeompointseqset_constructor(cursor, expected_tgeompointseqset):
    if isinstance(expected_tgeompointseqset, tuple):
        params = [TGeomPointSeqSet(*expected_tgeompointseqset)]
    else:
        params = [TGeomPointSeqSet(expected_tgeompointseqset)]
    cursor.execute('INSERT INTO tbl_tgeompointseqset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tgeompointseqset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tgeompointseqset, tuple):
        assert result == TGeomPointSeqSet(*expected_tgeompointseqset)
    else:
        assert result == TGeomPointSeqSet(expected_tgeompointseqset)

@pytest.mark.parametrize('expected_tgeompointseqset', [
    'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01],  '
    '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]}',
])
def test_tgeompointseqset_accessors(cursor, expected_tgeompointseqset):
    assert TGeomPointSeqSet(expected_tgeompointseqset).srid == 4326
    assert TGeomPointSeqSet(expected_tgeompointseqset).duration == TemporalDuration.SequenceSet
    assert TGeomPointSeqSet(expected_tgeompointseqset).duration.name == 'SequenceSet'
    assert TGeomPointSeqSet(expected_tgeompointseqset).getValues == \
        GeometryCollection([Point(10.0, 10.0), LineString([Point(20.0, 20.0), Point(30.0, 30.0)])])
    assert TGeomPointSeqSet(expected_tgeompointseqset).startValue == GeomPoint(10.0, 10.0, 4326)
    assert TGeomPointSeqSet(expected_tgeompointseqset).endValue == GeomPoint(30.0, 30.0, 4326)
    assert TGeomPointSeqSet(expected_tgeompointseqset).valueRange == RangeGeom(GeomPoint(10.0, 10.0, 4326), GeomPoint(30.0, 30.0, 4326), upper_inc=True)
    assert TGeomPointSeqSet(expected_tgeompointseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointSeqSet(expected_tgeompointseqset).timespan == timedelta(1)
    assert TGeomPointSeqSet(expected_tgeompointseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).numInstants == 3
    assert TGeomPointSeqSet(expected_tgeompointseqset).startInstant == TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).endInstant == TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).instantN(1) == TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).instants == {TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                        TGeomPointInst('SRID=4326;Point(30.0 30.0)@2019-09-03 00:00:00+01')}
    assert TGeomPointSeqSet(expected_tgeompointseqset).numTimestamps == 3
    assert TGeomPointSeqSet(expected_tgeompointseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')}
    assert TGeomPointSeqSet(expected_tgeompointseqset).numSequences == 2
    assert TGeomPointSeqSet(expected_tgeompointseqset).startSequence == TGeomPointSeq('SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).endSequence == TGeomPointSeq(
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).sequenceN(1) == TGeomPointSeq(
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).sequences == {TGeomPointSeq('SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')}
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TGeomPointSeqSet(expected_tgeompointseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
