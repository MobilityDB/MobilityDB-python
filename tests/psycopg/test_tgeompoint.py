###############################################################################
#
# This MobilityDB code is provided under The PostgreSQL License.
#
# Copyright (c) 2019-2021, Université libre de Bruxelles and MobilityDB
# contributors
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without a written 
# agreement is hereby granted, provided that the above copyright notice and
# this paragraph and the following two paragraphs appear in all copies.
#
# IN NO EVENT SHALL UNIVERSITE LIBRE DE BRUXELLES BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
# EVEN IF UNIVERSITE LIBRE DE BRUXELLES HAS BEEN ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.
#
# UNIVERSITE LIBRE DE BRUXELLES SPECIFICALLY DISCLAIMS ANY WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON
# AN "AS IS" BASIS, AND UNIVERSITE LIBRE DE BRUXELLES HAS NO OBLIGATIONS TO 
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS. 
#
###############################################################################

import pytest
from datetime import timedelta
from dateutil.parser import parse
from postgis import Point, MultiPoint, LineString, MultiLineString, GeometryCollection
from mobilitydb.main import TGeomPointInst, TGeomPointInstSet, TGeomPointSeq, TGeomPointSeqSet
from mobilitydb.time import TimestampSet, Period, PeriodSet


@pytest.mark.parametrize('expected_tgeompointinst', [
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
    assert TGeomPointInst(expected_tgeompointinst).tempSubtype() == 'Instant'
    assert TGeomPointInst(expected_tgeompointinst).getValue == Point(10.0, 10.0)
    assert TGeomPointInst(expected_tgeompointinst).getValues == Point(10.0, 10.0)
    assert TGeomPointInst(expected_tgeompointinst).startValue == Point(10.0, 10.0)
    assert TGeomPointInst(expected_tgeompointinst).endValue == Point(10.0, 10.0)
    assert TGeomPointInst(expected_tgeompointinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TGeomPointInst(expected_tgeompointinst).duration == timedelta(0)
    assert TGeomPointInst(expected_tgeompointinst).timespan == timedelta(0)
    assert TGeomPointInst(expected_tgeompointinst).period == Period(
        '[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TGeomPointInst(expected_tgeompointinst).numInstants == 1
    assert TGeomPointInst(expected_tgeompointinst).startInstant == TGeomPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).endInstant == TGeomPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).instantN(1) == TGeomPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).instants == [
        TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')]
    assert TGeomPointInst(expected_tgeompointinst).numTimestamps == 1
    assert TGeomPointInst(expected_tgeompointinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).timestampN(1) == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInst(expected_tgeompointinst).timestamps == [parse('2019-09-01 00:00:00+01')]
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
    ('Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'),
    ['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    ('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'),
    ['SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    (TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')),
    [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    (TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')),
    [TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
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
def test_tgeompointi_accessors(cursor, expected_tgeompointinstset):
    assert TGeomPointInstSet(expected_tgeompointinstset).srid == 4326
    assert TGeomPointInstSet(expected_tgeompointinstset).tempSubtype() == 'InstantSet'
    assert TGeomPointInstSet(expected_tgeompointinstset).getValues == \
           MultiPoint([Point(10.0, 10.0),Point(20.0, 20.0),Point(30.0, 30.0)])
    assert TGeomPointInstSet(expected_tgeompointinstset).startValue == Point(10.0, 10.0)
    assert TGeomPointInstSet(expected_tgeompointinstset).endValue == Point(30.0, 30.0)
    assert TGeomPointInstSet(expected_tgeompointinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointInstSet(expected_tgeompointinstset).duration == timedelta(0)
    assert TGeomPointInstSet(expected_tgeompointinstset).timespan == timedelta(2)
    assert TGeomPointInstSet(expected_tgeompointinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointInstSet(expected_tgeompointinstset).numInstants == 3
    assert TGeomPointInstSet(expected_tgeompointinstset).startInstant == TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).endInstant == TGeomPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).instantN(2) == TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).instants == [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                            TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                            TGeomPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')]
    assert TGeomPointInstSet(expected_tgeompointinstset).numTimestamps == 3
    assert TGeomPointInstSet(expected_tgeompointinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointInstSet(expected_tgeompointinstset).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                              parse('2019-09-02 00:00:00+01'),
                                                              parse('2019-09-03 00:00:00+01')]
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
    ['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    ['SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    [TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise'),
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Linear', 4326),
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise', 4326),
    ([TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
    ([TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
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
    assert TGeomPointSeq(expected_tgeompointseq).tempSubtype() == 'Sequence'
    assert TGeomPointSeq(expected_tgeompointseq).getValues == LineString([Point(10.0, 10.0),Point(20.0, 20.0),Point(10.0, 10.0)])
    assert TGeomPointSeq(expected_tgeompointseq).startValue == Point(10.0, 10.0)
    assert TGeomPointSeq(expected_tgeompointseq).endValue == Point(10.0, 10.0)
    assert TGeomPointSeq(expected_tgeompointseq).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointSeq(expected_tgeompointseq).duration == timedelta(2)
    assert TGeomPointSeq(expected_tgeompointseq).timespan == timedelta(2)
    assert TGeomPointSeq(expected_tgeompointseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointSeq(expected_tgeompointseq).numInstants == 3
    assert TGeomPointSeq(expected_tgeompointseq).startInstant == TGeomPointInst(
        'Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).endInstant == TGeomPointInst(
        'Point(10.0 10.0)@2019-09-03 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).instantN(2) == TGeomPointInst(
        'Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).instants == \
           [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
            TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
            TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')]
    assert TGeomPointSeq(expected_tgeompointseq).numTimestamps == 3
    assert TGeomPointSeq(expected_tgeompointseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointSeq(expected_tgeompointseq).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                                  parse('2019-09-02 00:00:00+01'),
                                                                  parse('2019-09-03 00:00:00+01')]
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
    [TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
    ([TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Linear'),
    ([TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq(
            'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
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
    assert TGeomPointSeqSet(expected_tgeompointseqset).tempSubtype() == 'SequenceSet'
    assert TGeomPointSeqSet(expected_tgeompointseqset).getValues == \
        GeometryCollection([Point(10.0, 10.0), LineString([Point(20.0, 20.0), Point(30.0, 30.0)])])
    assert TGeomPointSeqSet(expected_tgeompointseqset).startValue == Point(10.0, 10.0)
    assert TGeomPointSeqSet(expected_tgeompointseqset).endValue == Point(30.0, 30.0)
    # assert TGeomPointSeqSet(expected_tgeompointseqset).valueRange == geompointrange(Point(10.0, 10.0), Point(30.0, 30.0), upper_inc=True)
    assert TGeomPointSeqSet(expected_tgeompointseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TGeomPointSeqSet(expected_tgeompointseqset).duration == timedelta(1)
    assert TGeomPointSeqSet(expected_tgeompointseqset).timespan == timedelta(2)
    assert TGeomPointSeqSet(expected_tgeompointseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).numInstants == 3
    assert TGeomPointSeqSet(expected_tgeompointseqset).startInstant == TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).endInstant == TGeomPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).instantN(2) == TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).instants == [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
                                                        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
                                                        TGeomPointInst('Point(30.0 30.0)@2019-09-03 00:00:00+01')]
    assert TGeomPointSeqSet(expected_tgeompointseqset).numTimestamps == 3
    assert TGeomPointSeqSet(expected_tgeompointseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TGeomPointSeqSet(expected_tgeompointseqset).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')]
    assert TGeomPointSeqSet(expected_tgeompointseqset).numSequences == 2
    assert TGeomPointSeqSet(expected_tgeompointseqset).startSequence == TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).endSequence == TGeomPointSeq(
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).sequenceN(2) == TGeomPointSeq(
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')
    assert TGeomPointSeqSet(expected_tgeompointseqset).sequences == [TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(30.0 30.0)@2019-09-03 00:00:00+01]')]
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
