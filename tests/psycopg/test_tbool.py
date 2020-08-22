import pytest
from datetime import timedelta
from dateutil.parser import parse
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TBoolInst, TBoolInstSet, TBoolSeq, TBoolSeqSet

from pymeos.temporal import TemporalDuration
from pymeos.range import RangeBool


@pytest.mark.parametrize('expected_tboolinst', [
    'true@2019-09-01 00:00:00+01',
    ('true', '2019-09-08 00:00:00+01'),
    (True, parse('2019-09-08 00:00:00+01')),
])
def test_tboolinst_constructors(cursor, expected_tboolinst):
    params = [TBoolInst(expected_tboolinst)]
    cursor.execute('INSERT INTO tbl_tboolinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tboolinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TBoolInst(expected_tboolinst)

@pytest.mark.parametrize('expected_tboolinst', [
    'true@2019-09-01 00:00:00+01',
])
def test_tboolinst_accessors(cursor, expected_tboolinst):
    assert TBoolInst(expected_tboolinst).duration == TemporalDuration.Instant
    assert TBoolInst(expected_tboolinst).duration.name == 'Instant'
    assert TBoolInst(expected_tboolinst).getValue == True
    assert TBoolInst(expected_tboolinst).getValues == {RangeBool(True, True, True, True)}
    assert TBoolInst(expected_tboolinst).startValue == True
    assert TBoolInst(expected_tboolinst).endValue == True
    assert TBoolInst(expected_tboolinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TBoolInst(expected_tboolinst).timespan == timedelta(0)
    assert TBoolInst(expected_tboolinst).period == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TBoolInst(expected_tboolinst).numInstants == 1
    assert TBoolInst(expected_tboolinst).startInstant == TBoolInst('true@2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).endInstant == TBoolInst('true@2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).instantN(0) == TBoolInst('true@2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).instants == {TBoolInst('true@2019-09-01 00:00:00+01')}
    assert TBoolInst(expected_tboolinst).numTimestamps == 1
    assert TBoolInst(expected_tboolinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).timestampN(0) == parse('2019-09-01 00:00:00+01')
    assert TBoolInst(expected_tboolinst).timestamps == {parse('2019-09-01 00:00:00+01')}
    assert TBoolInst(expected_tboolinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TBoolInst(expected_tboolinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
    assert TBoolInst(expected_tboolinst).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TBoolInst(expected_tboolinst).intersectsTimestampSet(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TBoolInst(expected_tboolinst).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TBoolInst(expected_tboolinst).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TBoolInst(expected_tboolinst).intersectsPeriod(
        Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TBoolInst(expected_tboolinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TBoolInst(expected_tboolinst).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TBoolInst(expected_tboolinst).intersectsPeriodSet(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False

@pytest.mark.parametrize('expected_tboolinstset', [
    '{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
    {'true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'},
    {TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('true@2019-09-03 00:00:00+01')},
])
def test_tboolinstset_constructor(cursor, expected_tboolinstset):
    if isinstance(expected_tboolinstset, tuple):
        params = [TBoolInstSet(*expected_tboolinstset)]
    else:
        params = [TBoolInstSet(expected_tboolinstset)]
    cursor.execute('INSERT INTO tbl_tboolinstset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tboolinstset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tboolinstset, tuple):
        assert result == TBoolInstSet(*expected_tboolinstset)
    else:
        assert result == TBoolInstSet(expected_tboolinstset)

@pytest.mark.parametrize('expected_tboolinstset', [
    '{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
])
def test_tboolinstset_accessors(cursor, expected_tboolinstset):
    assert TBoolInstSet(expected_tboolinstset).duration == TemporalDuration.InstantSet
    assert TBoolInstSet(expected_tboolinstset).duration.name == 'InstantSet'
    assert TBoolInstSet(expected_tboolinstset).getValues == {RangeBool(True, True, True, True), RangeBool(False, False, True, True)}
    assert TBoolInstSet(expected_tboolinstset).startValue == True
    assert TBoolInstSet(expected_tboolinstset).endValue == True
    assert TBoolInstSet(expected_tboolinstset).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TBoolInstSet(expected_tboolinstset).timespan == timedelta(0)
    assert TBoolInstSet(expected_tboolinstset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TBoolInstSet(expected_tboolinstset).numInstants == 3
    assert TBoolInstSet(expected_tboolinstset).startInstant == TBoolInst('true@2019-09-01 00:00:00+01')
    assert TBoolInstSet(expected_tboolinstset).endInstant == TBoolInst('true@2019-09-03 00:00:00+01')
    assert TBoolInstSet(expected_tboolinstset).instantN(1) == TBoolInst('false@2019-09-02 00:00:00+01')
    assert TBoolInstSet(expected_tboolinstset).instants == {TBoolInst('true@2019-09-01 00:00:00+01'),
                                                TBoolInst('false@2019-09-02 00:00:00+01'),
                                                TBoolInst('true@2019-09-03 00:00:00+01')}
    assert TBoolInstSet(expected_tboolinstset).numTimestamps == 3
    assert TBoolInstSet(expected_tboolinstset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TBoolInstSet(expected_tboolinstset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TBoolInstSet(expected_tboolinstset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TBoolInstSet(expected_tboolinstset).timestamps == {parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')}
    assert TBoolInstSet(expected_tboolinstset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TBoolInstSet(expected_tboolinstset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TBoolInstSet(expected_tboolinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TBoolInstSet(expected_tboolinstset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TBoolInstSet(expected_tboolinstset).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TBoolInstSet(expected_tboolinstset).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TBoolInstSet(expected_tboolinstset).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TBoolInstSet(expected_tboolinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TBoolInstSet(expected_tboolinstset).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TBoolInstSet(expected_tboolinstset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False

@pytest.mark.parametrize('expected_tboolseq', [
    '[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, false@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, false@2019-09-03 00:00:00+01]',
    {'true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'false@2019-09-03 00:00:00+01'},
    {TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('false@2019-09-03 00:00:00+01')},
    ({'true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'}, True, True),
    ({TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
      TBoolInst('true@2019-09-03 00:00:00+01')}, True, True),
])
def test_tboolseq_constructor(cursor, expected_tboolseq):
    if isinstance(expected_tboolseq, tuple):
        params = [TBoolSeq(*expected_tboolseq)]
    else:
        params = [TBoolSeq(expected_tboolseq)]
    cursor.execute('INSERT INTO tbl_tboolseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tboolseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tboolseq, tuple):
        assert result == TBoolSeq(*expected_tboolseq)
    else:
        assert result == TBoolSeq(expected_tboolseq)


@pytest.mark.parametrize('expected_tboolseq', [
    '[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]',
])
def test_tboolseq_accessors(cursor, expected_tboolseq):
    assert TBoolSeq(expected_tboolseq).duration == TemporalDuration.Sequence
    assert TBoolSeq(expected_tboolseq).duration.name == 'Sequence'
    assert TBoolSeq(expected_tboolseq).getValues == {RangeBool(False, True, True, True)}
    assert TBoolSeq(expected_tboolseq).startValue == True
    assert TBoolSeq(expected_tboolseq).endValue == True
    assert TBoolSeq(expected_tboolseq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TBoolSeq(expected_tboolseq).timespan == timedelta(2)
    assert TBoolSeq(expected_tboolseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TBoolSeq(expected_tboolseq).numInstants == 3
    assert TBoolSeq(expected_tboolseq).startInstant == TBoolInst('true@2019-09-01 00:00:00+01')
    assert TBoolSeq(expected_tboolseq).endInstant == TBoolInst('true@2019-09-03 00:00:00+01')
    assert TBoolSeq(expected_tboolseq).instantN(1) == TBoolInst('false@2019-09-02 00:00:00+01')
    assert TBoolSeq(expected_tboolseq).instants == \
           {TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
            TBoolInst('true@2019-09-03 00:00:00+01')}
    assert TBoolSeq(expected_tboolseq).numTimestamps == 3
    assert TBoolSeq(expected_tboolseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TBoolSeq(expected_tboolseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TBoolSeq(expected_tboolseq).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TBoolSeq(expected_tboolseq).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                      parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')}
    assert TBoolSeq(expected_tboolseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TBoolSeq(expected_tboolseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TBoolSeq(expected_tboolseq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TBoolSeq(expected_tboolseq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TBoolSeq(expected_tboolseq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TBoolSeq(expected_tboolseq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TBoolSeq(expected_tboolseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TBoolSeq(expected_tboolseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tboolseqset', [
    '{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
    # 'Interp=Stepwise;{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
    {'[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'},
    {TBoolSeq('[true@2019-09-01 00:00:00+01]'),
     TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')},
])
def test_tboolseqset_constructor(cursor, expected_tboolseqset):
    if isinstance(expected_tboolseqset, tuple):
        params = [TBoolSeqSet(*expected_tboolseqset)]
    else:
        params = [TBoolSeqSet(expected_tboolseqset)]
    cursor.execute('INSERT INTO tbl_tboolseqset (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tboolseqset WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tboolseqset, tuple):
        assert result == TBoolSeqSet(*expected_tboolseqset)
    else:
        assert result == TBoolSeqSet(expected_tboolseqset)


@pytest.mark.parametrize('expected_tboolseqset', [
    '{[true@2019-09-01 00:00:00+01],  [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
])
def test_tboolseqset_accessors(cursor, expected_tboolseqset):
    assert TBoolSeqSet(expected_tboolseqset).duration == TemporalDuration.SequenceSet
    assert TBoolSeqSet(expected_tboolseqset).duration.name == 'SequenceSet'
    assert TBoolSeqSet(expected_tboolseqset).getValues == {RangeBool(True, True, True, True), RangeBool(False, True, True, True)}
    assert TBoolSeqSet(expected_tboolseqset).startValue == True
    assert TBoolSeqSet(expected_tboolseqset).endValue == True
    assert TBoolSeqSet(expected_tboolseqset).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TBoolSeqSet(expected_tboolseqset).timespan == timedelta(1)
    assert TBoolSeqSet(expected_tboolseqset).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TBoolSeqSet(expected_tboolseqset).numInstants == 3
    assert TBoolSeqSet(expected_tboolseqset).startInstant == TBoolInst('true@2019-09-01 00:00:00+01')
    assert TBoolSeqSet(expected_tboolseqset).endInstant == TBoolInst('true@2019-09-03 00:00:00+01')
    assert TBoolSeqSet(expected_tboolseqset).instantN(1) == TBoolInst('false@2019-09-02 00:00:00+01')
    assert TBoolSeqSet(expected_tboolseqset).instants == {TBoolInst('true@2019-09-01 00:00:00+01'),
                                                TBoolInst('false@2019-09-02 00:00:00+01'),
                                                TBoolInst('true@2019-09-03 00:00:00+01')}
    assert TBoolSeqSet(expected_tboolseqset).numTimestamps == 3
    assert TBoolSeqSet(expected_tboolseqset).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TBoolSeqSet(expected_tboolseqset).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TBoolSeqSet(expected_tboolseqset).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TBoolSeqSet(expected_tboolseqset).timestamps == {parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')}
    assert TBoolSeqSet(expected_tboolseqset).numSequences == 2
    assert TBoolSeqSet(expected_tboolseqset).startSequence == TBoolSeq('[true@2019-09-01 00:00:00+01]')
    assert TBoolSeqSet(expected_tboolseqset).endSequence == TBoolSeq(
        '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')
    assert TBoolSeqSet(expected_tboolseqset).sequenceN(1) == TBoolSeq(
        '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')
    assert TBoolSeqSet(expected_tboolseqset).sequences == {TBoolSeq('[true@2019-09-01 00:00:00+01]'),
                                                 TBoolSeq(
                                                     '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')}
    assert TBoolSeqSet(expected_tboolseqset).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TBoolSeqSet(expected_tboolseqset).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TBoolSeqSet(expected_tboolseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TBoolSeqSet(expected_tboolseqset).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TBoolSeqSet(expected_tboolseqset).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TBoolSeqSet(expected_tboolseqset).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TBoolSeqSet(expected_tboolseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TBoolSeqSet(expected_tboolseqset).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
