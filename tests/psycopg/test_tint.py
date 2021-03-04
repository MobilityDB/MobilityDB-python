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
from spans.types import intrange
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TIntInst, TIntInstSet, TIntSeq, TIntSeqSet


@pytest.mark.parametrize('expected_tintinst', [
    '10@2019-09-01 00:00:00+01',
    ('10', '2019-09-08 00:00:00+01'),
    ['10', '2019-09-08 00:00:00+01'],
    (10, parse('2019-09-08 00:00:00+01')),
    [10, parse('2019-09-08 00:00:00+01')],
])
def test_tintinst_constructors(cursor, expected_tintinst):
    params = [TIntInst(expected_tintinst)]
    cursor.execute('INSERT INTO tbl_tintinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tintinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TIntInst(expected_tintinst)


@pytest.mark.parametrize('expected_tintinst', [
    '10@2019-09-01 00:00:00+01',
])
def test_tintinst_accessors(cursor, expected_tintinst):
    assert TIntInst(expected_tintinst).tempSubtype() == 'Instant'
    assert TIntInst(expected_tintinst).getValue == 10
    assert TIntInst(expected_tintinst).getValues == [10]
    assert TIntInst(expected_tintinst).startValue == 10
    assert TIntInst(expected_tintinst).endValue == 10
    assert TIntInst(expected_tintinst).minValue == 10
    assert TIntInst(expected_tintinst).maxValue == 10
    assert TIntInst(expected_tintinst).valueRange == intrange(10, 10, upper_inc=True)
    assert TIntInst(expected_tintinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TIntInst(expected_tintinst).duration == timedelta(0)
    assert TIntInst(expected_tintinst).timespan == timedelta(0)
    assert TIntInst(expected_tintinst).period == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TIntInst(expected_tintinst).numInstants == 1
    assert TIntInst(expected_tintinst).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).endInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).instantN(1) == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).instants == [TIntInst('10@2019-09-01 00:00:00+01')]
    assert TIntInst(expected_tintinst).numTimestamps == 1
    assert TIntInst(expected_tintinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).timestampN(1) == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).timestamps == [parse('2019-09-01 00:00:00+01')]
    assert TIntInst(expected_tintinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TIntInst(expected_tintinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
    assert TIntInst(expected_tintinst).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TIntInst(expected_tintinst).intersectsTimestampSet(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TIntInst(expected_tintinst).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TIntInst(expected_tintinst).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TIntInst(expected_tintinst).intersectsPeriod(
        Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TIntInst(expected_tintinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TIntInst(expected_tintinst).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TIntInst(expected_tintinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tintinstset', [
    '{10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01}',
    ('10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'),
    (TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')),
    ['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'],
    [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')],
])
def test_tintinstset_constructor(cursor, expected_tintinstset):
    if isinstance(expected_tintinstset, tuple):
        params = [TIntInstSet(*expected_tintinstset)]
    else:
        params = [TIntInstSet(expected_tintinstset)]
    cursor.execute('INSERT INTO tbl_tintinstset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tintinstset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tintinstset, tuple):
        assert result == TIntInstSet(*expected_tintinstset)
    else:
        assert result == TIntInstSet(expected_tintinstset)


@pytest.mark.parametrize('expected_tintinstset', [
    '{10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01}',
])
def test_tintinstset_accessors(cursor, expected_tintinstset):
    assert TIntInstSet(expected_tintinstset).tempSubtype() == 'InstantSet'
    assert TIntInstSet(expected_tintinstset).getValues == [10, 20, 30]
    assert TIntInstSet(expected_tintinstset).startValue == 10
    assert TIntInstSet(expected_tintinstset).endValue == 30
    assert TIntInstSet(expected_tintinstset).minValue == 10
    assert TIntInstSet(expected_tintinstset).maxValue == 30
    assert TIntInstSet(expected_tintinstset).valueRange == intrange(10, 30, upper_inc=True)
    assert TIntInstSet(expected_tintinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TIntInstSet(expected_tintinstset).duration == timedelta(0)
    assert TIntInstSet(expected_tintinstset).timespan == timedelta(2)
    assert TIntInstSet(expected_tintinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TIntInstSet(expected_tintinstset).numInstants == 3
    assert TIntInstSet(expected_tintinstset).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).endInstant == TIntInst('30@2019-09-03 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).instantN(2) == TIntInst('20@2019-09-02 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).instants == [TIntInst('10@2019-09-01 00:00:00+01'),
                                                TIntInst('20@2019-09-02 00:00:00+01'),
                                                TIntInst('30@2019-09-03 00:00:00+01')]
    assert TIntInstSet(expected_tintinstset).numTimestamps == 3
    assert TIntInstSet(expected_tintinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')]
    assert TIntInstSet(expected_tintinstset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TIntInstSet(expected_tintinstset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TIntInstSet(expected_tintinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TIntInstSet(expected_tintinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TIntInstSet(expected_tintinstset).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TIntInstSet(expected_tintinstset).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TIntInstSet(expected_tintinstset).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TIntInstSet(expected_tintinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TIntInstSet(expected_tintinstset).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TIntInstSet(expected_tintinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tintseq', [
    '[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 20@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 20@2019-09-03 00:00:00+01]',
    ['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '20@2019-09-03 00:00:00+01'],
    [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('20@2019-09-03 00:00:00+01')],
    (['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'], True, True),
    ([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
      TIntInst('10@2019-09-03 00:00:00+01')], True, True),
])
def test_tintseq_constructor(cursor, expected_tintseq):
    if isinstance(expected_tintseq, tuple):
        params = [TIntSeq(*expected_tintseq)]
    else:
        params = [TIntSeq(expected_tintseq)]
    cursor.execute('INSERT INTO tbl_tintseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tintseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tintseq, tuple):
        assert result == TIntSeq(*expected_tintseq)
    else:
        assert result == TIntSeq(expected_tintseq)


@pytest.mark.parametrize('expected_tintseq', [
    '[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]',
])
def test_tintseq_accessors(cursor, expected_tintseq):
    assert TIntSeq(expected_tintseq).tempSubtype() == 'Sequence'
    assert TIntSeq(expected_tintseq).getValues == [10, 20, 30]
    assert TIntSeq(expected_tintseq).startValue == 10
    assert TIntSeq(expected_tintseq).endValue == 30
    assert TIntSeq(expected_tintseq).minValue == 10
    assert TIntSeq(expected_tintseq).maxValue == 30
    assert TIntSeq(expected_tintseq).valueRange == intrange(10, 30, upper_inc=True)
    assert TIntSeq(expected_tintseq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TIntSeq(expected_tintseq).duration == timedelta(2)
    assert TIntSeq(expected_tintseq).timespan == timedelta(2)
    assert TIntSeq(expected_tintseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TIntSeq(expected_tintseq).numInstants == 3
    assert TIntSeq(expected_tintseq).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntSeq(expected_tintseq).endInstant == TIntInst('30@2019-09-03 00:00:00+01')
    assert TIntSeq(expected_tintseq).instantN(2) == TIntInst('20@2019-09-02 00:00:00+01')
    assert TIntSeq(expected_tintseq).instants == \
           [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
            TIntInst('30@2019-09-03 00:00:00+01')]
    assert TIntSeq(expected_tintseq).numTimestamps == 3
    assert TIntSeq(expected_tintseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntSeq(expected_tintseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TIntSeq(expected_tintseq).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TIntSeq(expected_tintseq).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                      parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')]
    assert TIntSeq(expected_tintseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TIntSeq(expected_tintseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TIntSeq(expected_tintseq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TIntSeq(expected_tintseq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TIntSeq(expected_tintseq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TIntSeq(expected_tintseq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TIntSeq(expected_tintseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TIntSeq(expected_tintseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tintseqset', [
    '{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}',
    'Interp=Stepwise;{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}',
    ['[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'],
    [TIntSeq('[10@2019-09-01 00:00:00+01]'),
     TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')],
])
def test_tintseqset_constructor(cursor, expected_tintseqset):
    if isinstance(expected_tintseqset, tuple):
        params = [TIntSeqSet(*expected_tintseqset)]
    else:
        params = [TIntSeqSet(expected_tintseqset)]
    cursor.execute('INSERT INTO tbl_tintseqset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tintseqset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tintseqset, tuple):
        assert result == TIntSeqSet(*expected_tintseqset)
    else:
        assert result == TIntSeqSet(expected_tintseqset)


@pytest.mark.parametrize('expected_tintseqset', [
    '{[10@2019-09-01 00:00:00+01],  [20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]}',
])
def test_tintseqset_accessors(cursor, expected_tintseqset):
    assert TIntSeqSet(expected_tintseqset).tempSubtype() == 'SequenceSet'
    assert TIntSeqSet(expected_tintseqset).getValues == [10, 20, 30]
    assert TIntSeqSet(expected_tintseqset).startValue == 10
    assert TIntSeqSet(expected_tintseqset).endValue == 30
    assert TIntSeqSet(expected_tintseqset).minValue == 10
    assert TIntSeqSet(expected_tintseqset).maxValue == 30
    assert TIntSeqSet(expected_tintseqset).valueRange == intrange(10, 30, upper_inc=True)
    assert TIntSeqSet(expected_tintseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TIntSeqSet(expected_tintseqset).duration == timedelta(1)
    assert TIntSeqSet(expected_tintseqset).timespan == timedelta(2)
    assert TIntSeqSet(expected_tintseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).numInstants == 3
    assert TIntSeqSet(expected_tintseqset).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).endInstant == TIntInst('30@2019-09-03 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).instantN(2) == TIntInst('20@2019-09-02 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).instants == [TIntInst('10@2019-09-01 00:00:00+01'),
                                                TIntInst('20@2019-09-02 00:00:00+01'),
                                                TIntInst('30@2019-09-03 00:00:00+01')]
    assert TIntSeqSet(expected_tintseqset).numTimestamps == 3
    assert TIntSeqSet(expected_tintseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')]
    assert TIntSeqSet(expected_tintseqset).numSequences == 2
    assert TIntSeqSet(expected_tintseqset).startSequence == TIntSeq('[10@2019-09-01 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).endSequence == TIntSeq(
        '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).sequenceN(2) == TIntSeq(
        '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).sequences == [TIntSeq('[10@2019-09-01 00:00:00+01]'),
                                                 TIntSeq(
                                                     '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')]
    assert TIntSeqSet(expected_tintseqset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TIntSeqSet(expected_tintseqset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TIntSeqSet(expected_tintseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TIntSeqSet(expected_tintseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TIntSeqSet(expected_tintseqset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TIntSeqSet(expected_tintseqset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TIntSeqSet(expected_tintseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TIntSeqSet(expected_tintseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
