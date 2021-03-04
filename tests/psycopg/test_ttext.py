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
from mobilitydb.main import TTextInst, TTextInstSet, TTextSeq, TTextSeqSet
from mobilitydb.time import TimestampSet, Period, PeriodSet


@pytest.mark.parametrize('expected_ttextinst', [
    'AA@2019-09-01 00:00:00+01',
    ('AA', '2019-09-08 00:00:00+01'),
    ['AA', '2019-09-08 00:00:00+01'],
    ('AA', parse('2019-09-08 00:00:00+01')),
    ['AA', parse('2019-09-08 00:00:00+01')],
])
def test_ttextinst_constructors(cursor, expected_ttextinst):
    params = [TTextInst(expected_ttextinst)]
    cursor.execute('INSERT INTO tbl_ttextinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttextinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TTextInst(expected_ttextinst)


@pytest.mark.parametrize('expected_ttextinst', [
    'AA@2019-09-01 00:00:00+01',
])
def test_ttextinst_accessors(cursor, expected_ttextinst):
    assert TTextInst(expected_ttextinst).tempSubtype() == 'Instant'
    assert TTextInst(expected_ttextinst).getValue == 'AA'
    assert TTextInst(expected_ttextinst).getValues == ['AA']
    assert TTextInst(expected_ttextinst).startValue == 'AA'
    assert TTextInst(expected_ttextinst).endValue == 'AA'
    assert TTextInst(expected_ttextinst).minValue == 'AA'
    assert TTextInst(expected_ttextinst).maxValue == 'AA'
    assert TTextInst(expected_ttextinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TTextInst(expected_ttextinst).duration == timedelta(0)
    assert TTextInst(expected_ttextinst).timespan == timedelta(0)
    assert TTextInst(expected_ttextinst).period == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TTextInst(expected_ttextinst).numInstants == 1
    assert TTextInst(expected_ttextinst).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).endInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).instantN(1) == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).instants == [TTextInst('AA@2019-09-01 00:00:00+01')]
    assert TTextInst(expected_ttextinst).numTimestamps == 1
    assert TTextInst(expected_ttextinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).timestampN(1) == parse('2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).timestamps == [parse('2019-09-01 00:00:00+01')]
    assert TTextInst(expected_ttextinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextInst(expected_ttextinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
    assert TTextInst(expected_ttextinst).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextInst(expected_ttextinst).intersectsTimestampSet(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextInst(expected_ttextinst).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriod(
        Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextInst(expected_ttextinst).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False

@pytest.mark.parametrize('expected_ttextinstset', [
    '{AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01}',
    ('AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'),
    (TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('AA@2019-09-03 00:00:00+01')),
    ['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'],
    [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('AA@2019-09-03 00:00:00+01')],
])
def test_ttextinstset_constructor(cursor, expected_ttextinstset):
    if isinstance(expected_ttextinstset, tuple):
        params = [TTextInstSet(*expected_ttextinstset)]
    else:
        params = [TTextInstSet(expected_ttextinstset)]
    cursor.execute('INSERT INTO tbl_ttextinstset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttextinstset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_ttextinstset, tuple):
        assert result == TTextInstSet(*expected_ttextinstset)
    else:
        assert result == TTextInstSet(expected_ttextinstset)


@pytest.mark.parametrize('expected_ttextinstset', [
    '{AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01}',
])
def test_ttextinstset_accessors(cursor, expected_ttextinstset):
    assert TTextInstSet(expected_ttextinstset).tempSubtype() == 'InstantSet'
    assert TTextInstSet(expected_ttextinstset).getValues == ['AA', 'BB', 'CC']
    assert TTextInstSet(expected_ttextinstset).startValue == 'AA'
    assert TTextInstSet(expected_ttextinstset).endValue == 'CC'
    assert TTextInstSet(expected_ttextinstset).minValue == 'AA'
    assert TTextInstSet(expected_ttextinstset).maxValue == 'CC'
    assert TTextInstSet(expected_ttextinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TTextInstSet(expected_ttextinstset).duration == timedelta(0)
    assert TTextInstSet(expected_ttextinstset).timespan == timedelta(2)
    assert TTextInstSet(expected_ttextinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TTextInstSet(expected_ttextinstset).numInstants == 3
    assert TTextInstSet(expected_ttextinstset).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextInstSet(expected_ttextinstset).endInstant == TTextInst('CC@2019-09-03 00:00:00+01')
    assert TTextInstSet(expected_ttextinstset).instantN(2) == TTextInst('BB@2019-09-02 00:00:00+01')
    assert TTextInstSet(expected_ttextinstset).instants == [TTextInst('AA@2019-09-01 00:00:00+01'),
                                                TTextInst('BB@2019-09-02 00:00:00+01'),
                                                TTextInst('CC@2019-09-03 00:00:00+01')]
    assert TTextInstSet(expected_ttextinstset).numTimestamps == 3
    assert TTextInstSet(expected_ttextinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextInstSet(expected_ttextinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TTextInstSet(expected_ttextinstset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TTextInstSet(expected_ttextinstset).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')]
    assert TTextInstSet(expected_ttextinstset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextInstSet(expected_ttextinstset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TTextInstSet(expected_ttextinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextInstSet(expected_ttextinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TTextInstSet(expected_ttextinstset).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextInstSet(expected_ttextinstset).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TTextInstSet(expected_ttextinstset).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TTextInstSet(expected_ttextinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextInstSet(expected_ttextinstset).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TTextInstSet(expected_ttextinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_ttextseqseteq', [
    '[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, BB@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, BB@2019-09-03 00:00:00+01]',
    ['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'BB@2019-09-03 00:00:00+01'],
    [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('BB@2019-09-03 00:00:00+01')],
    (['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'], True, True),
    ([TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
      TTextInst('AA@2019-09-03 00:00:00+01')], True, True),
])
def test_ttextseq_constructor(cursor, expected_ttextseqseteq):
    if isinstance(expected_ttextseqseteq, tuple):
        params = [TTextSeq(*expected_ttextseqseteq)]
    else:
        params = [TTextSeq(expected_ttextseqseteq)]
    cursor.execute('INSERT INTO tbl_ttextseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttextseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_ttextseqseteq, tuple):
        assert result == TTextSeq(*expected_ttextseqseteq)
    else:
        assert result == TTextSeq(expected_ttextseqseteq)


@pytest.mark.parametrize('expected_ttextseqseteq', [
    '[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]',
])
def test_ttextseq_accessors(cursor, expected_ttextseqseteq):
    assert TTextSeq(expected_ttextseqseteq).tempSubtype() == 'Sequence'
    assert TTextSeq(expected_ttextseqseteq).getValues == ['AA', 'BB', 'CC']
    assert TTextSeq(expected_ttextseqseteq).startValue == 'AA'
    assert TTextSeq(expected_ttextseqseteq).endValue == 'CC'
    assert TTextSeq(expected_ttextseqseteq).minValue == 'AA'
    assert TTextSeq(expected_ttextseqseteq).maxValue == 'CC'
    assert TTextSeq(expected_ttextseqseteq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TTextSeq(expected_ttextseqseteq).duration == timedelta(2)
    assert TTextSeq(expected_ttextseqseteq).timespan == timedelta(2)
    assert TTextSeq(expected_ttextseqseteq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TTextSeq(expected_ttextseqseteq).numInstants == 3
    assert TTextSeq(expected_ttextseqseteq).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextSeq(expected_ttextseqseteq).endInstant == TTextInst('CC@2019-09-03 00:00:00+01')
    assert TTextSeq(expected_ttextseqseteq).instantN(2) == TTextInst('BB@2019-09-02 00:00:00+01')
    assert TTextSeq(expected_ttextseqseteq).instants == \
           [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
            TTextInst('CC@2019-09-03 00:00:00+01')]
    assert TTextSeq(expected_ttextseqseteq).numTimestamps == 3
    assert TTextSeq(expected_ttextseqseteq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextSeq(expected_ttextseqseteq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TTextSeq(expected_ttextseqseteq).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TTextSeq(expected_ttextseqseteq).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                      parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')]
    assert TTextSeq(expected_ttextseqseteq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextSeq(expected_ttextseqseteq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TTextSeq(expected_ttextseqseteq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextSeq(expected_ttextseqseteq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TTextSeq(expected_ttextseqseteq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextSeq(expected_ttextseqseteq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TTextSeq(expected_ttextseqseteq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextSeq(expected_ttextseqseteq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_ttextseqset', [
    '{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}',
    'Interp=Stepwise;{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}',
    ['[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'],
    [TTextSeq('[AA@2019-09-01 00:00:00+01]'),
     TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')],
])
def test_ttextseqset_constructor(cursor, expected_ttextseqset):
    if isinstance(expected_ttextseqset, tuple):
        params = [TTextSeqSet(*expected_ttextseqset)]
    else:
        params = [TTextSeqSet(expected_ttextseqset)]
    cursor.execute('INSERT INTO tbl_ttextseqset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttextseqset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_ttextseqset, tuple):
        assert result == TTextSeqSet(*expected_ttextseqset)
    else:
        assert result == TTextSeqSet(expected_ttextseqset)


@pytest.mark.parametrize('expected_ttextseqset', [
    '{[AA@2019-09-01 00:00:00+01],  [BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]}',
])
def test_ttextseqset_accessors(cursor, expected_ttextseqset):
    assert TTextSeqSet(expected_ttextseqset).tempSubtype() == 'SequenceSet'
    assert TTextSeqSet(expected_ttextseqset).getValues == ['AA', 'BB', 'CC']
    assert TTextSeqSet(expected_ttextseqset).startValue == 'AA'
    assert TTextSeqSet(expected_ttextseqset).endValue == 'CC'
    assert TTextSeqSet(expected_ttextseqset).minValue == 'AA'
    assert TTextSeqSet(expected_ttextseqset).maxValue == 'CC'
    assert TTextSeqSet(expected_ttextseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TTextSeqSet(expected_ttextseqset).duration == timedelta(1)
    assert TTextSeqSet(expected_ttextseqset).timespan == timedelta(2)
    assert TTextSeqSet(expected_ttextseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TTextSeqSet(expected_ttextseqset).numInstants == 3
    assert TTextSeqSet(expected_ttextseqset).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextSeqSet(expected_ttextseqset).endInstant == TTextInst('CC@2019-09-03 00:00:00+01')
    assert TTextSeqSet(expected_ttextseqset).instantN(2) == TTextInst('BB@2019-09-02 00:00:00+01')
    assert TTextSeqSet(expected_ttextseqset).instants == [TTextInst('AA@2019-09-01 00:00:00+01'),
                                                TTextInst('BB@2019-09-02 00:00:00+01'),
                                                TTextInst('CC@2019-09-03 00:00:00+01')]
    assert TTextSeqSet(expected_ttextseqset).numTimestamps == 3
    assert TTextSeqSet(expected_ttextseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextSeqSet(expected_ttextseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TTextSeqSet(expected_ttextseqset).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TTextSeqSet(expected_ttextseqset).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')]
    assert TTextSeqSet(expected_ttextseqset).numSequences == 2
    assert TTextSeqSet(expected_ttextseqset).startSequence == TTextSeq('[AA@2019-09-01 00:00:00+01]')
    assert TTextSeqSet(expected_ttextseqset).endSequence == TTextSeq(
        '[BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]')
    assert TTextSeqSet(expected_ttextseqset).sequenceN(2) == TTextSeq(
        '[BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]')
    assert TTextSeqSet(expected_ttextseqset).sequences == [TTextSeq('[AA@2019-09-01 00:00:00+01]'),
                                                 TTextSeq(
                                                     '[BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]')]
    assert TTextSeqSet(expected_ttextseqset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextSeqSet(expected_ttextseqset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TTextSeqSet(expected_ttextseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextSeqSet(expected_ttextseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TTextSeqSet(expected_ttextseqset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextSeqSet(expected_ttextseqset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TTextSeqSet(expected_ttextseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextSeqSet(expected_ttextseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
