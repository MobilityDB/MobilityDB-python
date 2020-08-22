from datetime import timedelta
from dateutil.parser import parse

import pytest
from pymeos.temporal import TemporalDuration
from pymeos.range import RangeInt

from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TIntInst, TIntInstSet, TIntSeq, TIntSeqSet


@pytest.mark.parametrize('expected_tintinst', [
    '10@2019-09-01 00:00:00+01',
    ('10', '2019-09-08 00:00:00+01'),
    (10, parse('2019-09-08 00:00:00+01')),
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
    assert TIntInst(expected_tintinst).duration == TemporalDuration.Instant
    assert TIntInst(expected_tintinst).duration.name == 'Instant'
    assert TIntInst(expected_tintinst).getValue == 10
    assert TIntInst(expected_tintinst).getValues == {RangeInt(10, 10, True, True)}
    assert TIntInst(expected_tintinst).startValue == 10
    assert TIntInst(expected_tintinst).endValue == 10
    assert TIntInst(expected_tintinst).minValue == 10
    assert TIntInst(expected_tintinst).maxValue == 10
    assert TIntInst(expected_tintinst).valueRange == RangeInt(10, 10, upper_inc=True)
    assert TIntInst(expected_tintinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TIntInst(expected_tintinst).timespan == timedelta(0)
    assert TIntInst(expected_tintinst).period == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TIntInst(expected_tintinst).numInstants == 1
    assert TIntInst(expected_tintinst).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).endInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).instantN(0) == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).instants == {TIntInst('10@2019-09-01 00:00:00+01')}
    assert TIntInst(expected_tintinst).numTimestamps == 1
    assert TIntInst(expected_tintinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).timestampN(0) == parse('2019-09-01 00:00:00+01')
    assert TIntInst(expected_tintinst).timestamps == {parse('2019-09-01 00:00:00+01')}
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
    {'10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'},
    {TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('10@2019-09-03 00:00:00+01')},
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
    assert TIntInstSet(expected_tintinstset).duration == TemporalDuration.InstantSet
    assert TIntInstSet(expected_tintinstset).duration.name == 'InstantSet'
    assert TIntInstSet(expected_tintinstset).getValues == {RangeInt(10, 10, True, True), RangeInt(20, 20, True, True), RangeInt(30, 30, True, True)}
    assert TIntInstSet(expected_tintinstset).startValue == 10
    assert TIntInstSet(expected_tintinstset).endValue == 30
    assert TIntInstSet(expected_tintinstset).minValue == 10
    assert TIntInstSet(expected_tintinstset).maxValue == 30
    assert TIntInstSet(expected_tintinstset).valueRange == RangeInt(10, 30, upper_inc=True)
    assert TIntInstSet(expected_tintinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TIntInstSet(expected_tintinstset).timespan == timedelta(0)
    assert TIntInstSet(expected_tintinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TIntInstSet(expected_tintinstset).numInstants == 3
    assert TIntInstSet(expected_tintinstset).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).endInstant == TIntInst('30@2019-09-03 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).instantN(1) == TIntInst('20@2019-09-02 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).instants == {TIntInst('10@2019-09-01 00:00:00+01'),
                                                TIntInst('20@2019-09-02 00:00:00+01'),
                                                TIntInst('30@2019-09-03 00:00:00+01')}
    assert TIntInstSet(expected_tintinstset).numTimestamps == 3
    assert TIntInstSet(expected_tintinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TIntInstSet(expected_tintinstset).timestamps == {parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')}
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
    {'10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '20@2019-09-03 00:00:00+01'},
    {TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
     TIntInst('20@2019-09-03 00:00:00+01')},
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
    assert TIntSeq(expected_tintseq).duration == TemporalDuration.Sequence
    assert TIntSeq(expected_tintseq).duration.name == 'Sequence'
    assert TIntSeq(expected_tintseq).getValues == {RangeInt(10, 30, True, True)}
    assert TIntSeq(expected_tintseq).startValue == 10
    assert TIntSeq(expected_tintseq).endValue == 30
    assert TIntSeq(expected_tintseq).minValue == 10
    assert TIntSeq(expected_tintseq).maxValue == 30
    assert TIntSeq(expected_tintseq).valueRange == RangeInt(10, 30, upper_inc=True)
    assert TIntSeq(expected_tintseq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TIntSeq(expected_tintseq).timespan == timedelta(2)
    assert TIntSeq(expected_tintseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TIntSeq(expected_tintseq).numInstants == 3
    assert TIntSeq(expected_tintseq).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntSeq(expected_tintseq).endInstant == TIntInst('30@2019-09-03 00:00:00+01')
    assert TIntSeq(expected_tintseq).instantN(1) == TIntInst('20@2019-09-02 00:00:00+01')
    assert TIntSeq(expected_tintseq).instants == \
           {TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
            TIntInst('30@2019-09-03 00:00:00+01')}
    assert TIntSeq(expected_tintseq).numTimestamps == 3
    assert TIntSeq(expected_tintseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntSeq(expected_tintseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TIntSeq(expected_tintseq).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TIntSeq(expected_tintseq).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                      parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')}
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
    {'[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'},
    {TIntSeq('[10@2019-09-01 00:00:00+01]'),
     TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')},
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
    assert TIntSeqSet(expected_tintseqset).duration == TemporalDuration.SequenceSet
    assert TIntSeqSet(expected_tintseqset).duration.name == 'SequenceSet'
    assert TIntSeqSet(expected_tintseqset).getValues == {RangeInt(10, 10, True, True), RangeInt(20, 30, True, True)}
    assert TIntSeqSet(expected_tintseqset).startValue == 10
    assert TIntSeqSet(expected_tintseqset).endValue == 30
    assert TIntSeqSet(expected_tintseqset).minValue == 10
    assert TIntSeqSet(expected_tintseqset).maxValue == 30
    assert TIntSeqSet(expected_tintseqset).valueRange == RangeInt(10, 30, upper_inc=True)
    assert TIntSeqSet(expected_tintseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TIntSeqSet(expected_tintseqset).timespan == timedelta(1)
    assert TIntSeqSet(expected_tintseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).numInstants == 3
    assert TIntSeqSet(expected_tintseqset).startInstant == TIntInst('10@2019-09-01 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).endInstant == TIntInst('30@2019-09-03 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).instantN(1) == TIntInst('20@2019-09-02 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).instants == {TIntInst('10@2019-09-01 00:00:00+01'),
                                                TIntInst('20@2019-09-02 00:00:00+01'),
                                                TIntInst('30@2019-09-03 00:00:00+01')}
    assert TIntSeqSet(expected_tintseqset).numTimestamps == 3
    assert TIntSeqSet(expected_tintseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TIntSeqSet(expected_tintseqset).timestamps == {parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')}
    assert TIntSeqSet(expected_tintseqset).numSequences == 2
    assert TIntSeqSet(expected_tintseqset).startSequence == TIntSeq('[10@2019-09-01 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).endSequence == TIntSeq(
        '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).sequenceN(1) == TIntSeq(
        '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')
    assert TIntSeqSet(expected_tintseqset).sequences == {TIntSeq('[10@2019-09-01 00:00:00+01]'),
                                                 TIntSeq(
                                                     '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')}
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
