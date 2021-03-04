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
from spans.types import floatrange
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TFloatInst, TFloatInstSet, TFloatSeq, TFloatSeqSet


@pytest.mark.parametrize('expected_tfloatinst', [
    '10.0@2019-09-01 00:00:00+01',
    ('10.0', '2019-09-08 00:00:00+01'),
    ['10.0', '2019-09-08 00:00:00+01'],
    (10.0, parse('2019-09-08 00:00:00+01')),
    [10.0, parse('2019-09-08 00:00:00+01')],
])
def test_tfloatinst_constructors(cursor, expected_tfloatinst):
    params = [TFloatInst(expected_tfloatinst)]
    cursor.execute('INSERT INTO tbl_tfloatinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFloatInst(expected_tfloatinst)

@pytest.mark.parametrize('expected_tfloatinst', [
    '10.0@2019-09-01 00:00:00+01',
])
def test_tfloatinst_accessors(cursor, expected_tfloatinst):
    assert TFloatInst(expected_tfloatinst).tempSubtype() == 'Instant'
    assert TFloatInst(expected_tfloatinst).getValue == 10.0
    assert TFloatInst(expected_tfloatinst).getValues == [floatrange(10.0, 10.0, upper_inc=True)]
    assert TFloatInst(expected_tfloatinst).startValue == 10.0
    assert TFloatInst(expected_tfloatinst).endValue == 10.0
    assert TFloatInst(expected_tfloatinst).minValue == 10.0
    assert TFloatInst(expected_tfloatinst).maxValue == 10.0
    assert TFloatInst(expected_tfloatinst).valueRange == floatrange(10.0, 10.0, upper_inc=True)
    assert TFloatInst(expected_tfloatinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TFloatInst(expected_tfloatinst).duration == timedelta(0)
    assert TFloatInst(expected_tfloatinst).timespan == timedelta(0)
    assert TFloatInst(expected_tfloatinst).period == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TFloatInst(expected_tfloatinst).numInstants == 1
    assert TFloatInst(expected_tfloatinst).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).endInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).instantN(1) == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).instants == [TFloatInst('10.0@2019-09-01 00:00:00+01')]
    assert TFloatInst(expected_tfloatinst).numTimestamps == 1
    assert TFloatInst(expected_tfloatinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).timestampN(1) == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).timestamps == [parse('2019-09-01 00:00:00+01')]
    assert TFloatInst(expected_tfloatinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatInst(expected_tfloatinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
    assert TFloatInst(expected_tfloatinst).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatInst(expected_tfloatinst).intersectsTimestampSet(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TFloatInst(expected_tfloatinst).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatInst(expected_tfloatinst).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TFloatInst(expected_tfloatinst).intersectsPeriod(Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TFloatInst(expected_tfloatinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatInst(expected_tfloatinst).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TFloatInst(expected_tfloatinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tfloatinstset', [
    '{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01}',
    ('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
    (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
     TFloatInst('10.0@2019-09-03 00:00:00+01')),
    ['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
    [TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
     TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
def test_tfloatinstset_constructor(cursor, expected_tfloatinstset):
    if isinstance(expected_tfloatinstset, tuple):
        params = [TFloatInstSet(*expected_tfloatinstset)]
    else:
        params = [TFloatInstSet(expected_tfloatinstset)]
    cursor.execute('INSERT INTO tbl_tfloatinstset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatinstset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tfloatinstset, tuple):
        assert result == TFloatInstSet(*expected_tfloatinstset)
    else:
        assert result == TFloatInstSet(expected_tfloatinstset)


@pytest.mark.parametrize('expected_tfloatinstset', [
    '{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01}',
])
def test_tfloatinstset_accessors(cursor, expected_tfloatinstset):
    assert TFloatInstSet(expected_tfloatinstset).tempSubtype() == 'InstantSet'
    assert TFloatInstSet(expected_tfloatinstset).getValues == [floatrange(10.0, 10.0, upper_inc=True),
                                             floatrange(20.0, 20.0, upper_inc=True),
                                             floatrange(30.0, 30.0, upper_inc=True)]
    assert TFloatInstSet(expected_tfloatinstset).startValue == 10.0
    assert TFloatInstSet(expected_tfloatinstset).endValue == 30.0
    assert TFloatInstSet(expected_tfloatinstset).minValue == 10.0
    assert TFloatInstSet(expected_tfloatinstset).maxValue == 30.0
    assert TFloatInstSet(expected_tfloatinstset).valueRange == floatrange(10.0, 30.0, upper_inc=True)
    assert TFloatInstSet(expected_tfloatinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TFloatInstSet(expected_tfloatinstset).duration == timedelta(0)
    assert TFloatInstSet(expected_tfloatinstset).timespan == timedelta(2)
    assert TFloatInstSet(expected_tfloatinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TFloatInstSet(expected_tfloatinstset).numInstants == 3
    assert TFloatInstSet(expected_tfloatinstset).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInstSet(expected_tfloatinstset).endInstant == TFloatInst('30.0@2019-09-03 00:00:00+01')
    assert TFloatInstSet(expected_tfloatinstset).instantN(2) == TFloatInst('20.0@2019-09-02 00:00:00+01')
    assert TFloatInstSet(expected_tfloatinstset).instants == [TFloatInst('10.0@2019-09-01 00:00:00+01'),
                                            TFloatInst('20.0@2019-09-02 00:00:00+01'),
                                            TFloatInst('30.0@2019-09-03 00:00:00+01')]
    assert TFloatInstSet(expected_tfloatinstset).numTimestamps == 3
    assert TFloatInstSet(expected_tfloatinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInstSet(expected_tfloatinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TFloatInstSet(expected_tfloatinstset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TFloatInstSet(expected_tfloatinstset).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                              parse('2019-09-03 00:00:00+01')]
    assert TFloatInstSet(expected_tfloatinstset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatInstSet(expected_tfloatinstset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TFloatInstSet(expected_tfloatinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatInstSet(expected_tfloatinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TFloatInstSet(expected_tfloatinstset).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatInstSet(expected_tfloatinstset).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TFloatInstSet(expected_tfloatinstset).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TFloatInstSet(expected_tfloatinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatInstSet(expected_tfloatinstset).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TFloatInstSet(expected_tfloatinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tfloatseqseteq', [
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
def test_tfloatseq_constructor(cursor, expected_tfloatseqseteq):
    if isinstance(expected_tfloatseqseteq, tuple):
        params = [TFloatSeq(*expected_tfloatseqseteq)]
    else:
        params = [TFloatSeq(expected_tfloatseqseteq)]
    cursor.execute('INSERT INTO tbl_tfloatseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tfloatseqseteq, tuple):
        assert result == TFloatSeq(*expected_tfloatseqseteq)
    else:
        assert result == TFloatSeq(expected_tfloatseqseteq)


@pytest.mark.parametrize('expected_tfloatseqseteq', [
    '[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]',
])
def test_tfloatseq_accessors(cursor, expected_tfloatseqseteq):
    assert TFloatSeq(expected_tfloatseqseteq).tempSubtype() == 'Sequence'
    # assert TFloatSeq(expected_tfloatseqseteq).getValues == [floatrange(10.0, 30.0, upper_inc=True)]
    assert TFloatSeq(expected_tfloatseqseteq).startValue == 10.0
    assert TFloatSeq(expected_tfloatseqseteq).endValue == 30.0
    assert TFloatSeq(expected_tfloatseqseteq).minValue == 10.0
    assert TFloatSeq(expected_tfloatseqseteq).maxValue == 30.0
    assert TFloatSeq(expected_tfloatseqseteq).valueRange == floatrange(10.0, 30.0, upper_inc=True)
    assert TFloatSeq(expected_tfloatseqseteq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TFloatSeq(expected_tfloatseqseteq).duration == timedelta(2)
    assert TFloatSeq(expected_tfloatseqseteq).timespan == timedelta(2)
    assert TFloatSeq(expected_tfloatseqseteq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TFloatSeq(expected_tfloatseqseteq).numInstants == 3
    assert TFloatSeq(expected_tfloatseqseteq).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatSeq(expected_tfloatseqseteq).endInstant == TFloatInst('30.0@2019-09-03 00:00:00+01')
    assert TFloatSeq(expected_tfloatseqseteq).instantN(2) == TFloatInst('20.0@2019-09-02 00:00:00+01')
    assert TFloatSeq(expected_tfloatseqseteq).instants == \
           [TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
            TFloatInst('30.0@2019-09-03 00:00:00+01')]
    assert TFloatSeq(expected_tfloatseqseteq).numTimestamps == 3
    assert TFloatSeq(expected_tfloatseqseteq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatSeq(expected_tfloatseqseteq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TFloatSeq(expected_tfloatseqseteq).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TFloatSeq(expected_tfloatseqseteq).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')]
    assert TFloatSeq(expected_tfloatseqseteq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatSeq(expected_tfloatseqseteq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TFloatSeq(expected_tfloatseqseteq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatSeq(expected_tfloatseqseteq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TFloatSeq(expected_tfloatseqseteq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatSeq(expected_tfloatseqseteq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TFloatSeq(expected_tfloatseqseteq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatSeq(expected_tfloatseqseteq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tfloatseqset', [
    '{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
    'Interp=Stepwise;{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
    ['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'],
    (['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'], 'Linear'),
    (['Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'], 'Stepwise'),
    [TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
     TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')],
    ([TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
      TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')], 'Linear'),
    ([TFloatSeq('Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]'),
      TFloatSeq('Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')], 'Stepwise'),
])
def test_tfloatseqset_constructor(cursor, expected_tfloatseqset):
    if isinstance(expected_tfloatseqset, tuple):
        params = [TFloatSeqSet(*expected_tfloatseqset)]
    else:
        params = [TFloatSeqSet(expected_tfloatseqset)]
    cursor.execute('INSERT INTO tbl_tfloatseqset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatseqset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tfloatseqset, tuple):
        assert result == TFloatSeqSet(*expected_tfloatseqset)
    else:
        assert result == TFloatSeqSet(expected_tfloatseqset)


@pytest.mark.parametrize('expected_tfloatseqset', [
    '{[10.0@2019-09-01 00:00:00+01],  [20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]}',
])
def test_tfloatseqset_accessors(cursor, expected_tfloatseqset):
    assert TFloatSeqSet(expected_tfloatseqset).tempSubtype() == 'SequenceSet'
    #assert TFloatSeqSet(expected_tfloatseqset).getValues == [floatrange(10.0, 10.0, upper_inc=True),floatrange(20.0, 30.0, 30.0, upper_inc=True)]
    assert TFloatSeqSet(expected_tfloatseqset).startValue == 10.0
    assert TFloatSeqSet(expected_tfloatseqset).endValue == 30.0
    assert TFloatSeqSet(expected_tfloatseqset).minValue == 10.0
    assert TFloatSeqSet(expected_tfloatseqset).maxValue == 30.0
    assert TFloatSeqSet(expected_tfloatseqset).valueRange == floatrange(10.0, 30.0, upper_inc=True)
    assert TFloatSeqSet(expected_tfloatseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TFloatSeqSet(expected_tfloatseqset).duration == timedelta(1)
    assert TFloatSeqSet(expected_tfloatseqset).timespan == timedelta(2)
    assert TFloatSeqSet(expected_tfloatseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TFloatSeqSet(expected_tfloatseqset).numInstants == 3
    assert TFloatSeqSet(expected_tfloatseqset).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatSeqSet(expected_tfloatseqset).endInstant == TFloatInst('30.0@2019-09-03 00:00:00+01')
    assert TFloatSeqSet(expected_tfloatseqset).instantN(2) == TFloatInst('20.0@2019-09-02 00:00:00+01')
    assert TFloatSeqSet(expected_tfloatseqset).instants == [TFloatInst('10.0@2019-09-01 00:00:00+01'),
                                                    TFloatInst('20.0@2019-09-02 00:00:00+01'),
                                                    TFloatInst('30.0@2019-09-03 00:00:00+01')]
    assert TFloatSeqSet(expected_tfloatseqset).numTimestamps == 3
    assert TFloatSeqSet(expected_tfloatseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatSeqSet(expected_tfloatseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TFloatSeqSet(expected_tfloatseqset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TFloatSeqSet(expected_tfloatseqset).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')]
    assert TFloatSeqSet(expected_tfloatseqset).numSequences == 2
    assert TFloatSeqSet(expected_tfloatseqset).startSequence == TFloatSeq('[10.0@2019-09-01 00:00:00+01]')
    assert TFloatSeqSet(expected_tfloatseqset).endSequence == TFloatSeq(
        '[20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]')
    assert TFloatSeqSet(expected_tfloatseqset).sequenceN(2) == TFloatSeq(
        '[20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]')
    assert TFloatSeqSet(expected_tfloatseqset).sequences == [TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
                                                     TFloatSeq(
                                                         '[20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]')]
    assert TFloatSeqSet(expected_tfloatseqset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatSeqSet(expected_tfloatseqset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TFloatSeqSet(expected_tfloatseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatSeqSet(expected_tfloatseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TFloatSeqSet(expected_tfloatseqset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatSeqSet(expected_tfloatseqset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TFloatSeqSet(expected_tfloatseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatSeqSet(expected_tfloatseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
