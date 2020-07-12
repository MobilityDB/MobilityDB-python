import pytest
from datetime import timedelta
from dateutil.parser import parse
from spans.types import floatrange
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TFloatInst, TFloatI, TFloatSeq, TFloatS

from pymeos.temporal import TemporalDuration
from pymeos.range import RangeFloat

@pytest.mark.parametrize('expected_tfloatinst', [
    '10.0@2019-09-01 00:00:00+01',
    ('10.0', '2019-09-08 00:00:00+01'),
    (10.0, parse('2019-09-08 00:00:00+01')),
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
    assert TFloatInst(expected_tfloatinst).duration == TemporalDuration.Instant
    assert TFloatInst(expected_tfloatinst).duration.name == 'Instant'
    assert TFloatInst(expected_tfloatinst).getValue == 10.0
    assert TFloatInst(expected_tfloatinst).getValues == {RangeFloat(10.0, 10.0, upper_inc=True)}
    assert TFloatInst(expected_tfloatinst).startValue == 10.0
    assert TFloatInst(expected_tfloatinst).endValue == 10.0
    assert TFloatInst(expected_tfloatinst).minValue == 10.0
    assert TFloatInst(expected_tfloatinst).maxValue == 10.0
    assert TFloatInst(expected_tfloatinst).valueRange == floatrange(10.0, 10.0, upper_inc=True)
    assert TFloatInst(expected_tfloatinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
    assert TFloatInst(expected_tfloatinst).timespan == timedelta(0)
    assert TFloatInst(expected_tfloatinst).period == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
    assert TFloatInst(expected_tfloatinst).numInstants == 1
    assert TFloatInst(expected_tfloatinst).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).endInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).instantN(0) == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).instants == {TFloatInst('10.0@2019-09-01 00:00:00+01')}
    assert TFloatInst(expected_tfloatinst).numTimestamps == 1
    assert TFloatInst(expected_tfloatinst).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).endTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).timestampN(0) == parse('2019-09-01 00:00:00+01')
    assert TFloatInst(expected_tfloatinst).timestamps == {parse('2019-09-01 00:00:00+01')}
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


@pytest.mark.parametrize('expected_tfloati', [
    '{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01}',
    {'10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'},
    {TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
     TFloatInst('10.0@2019-09-03 00:00:00+01')},
])
def test_tfloati_constructor(cursor, expected_tfloati):
    if isinstance(expected_tfloati, tuple):
        params = [TFloatI(*expected_tfloati)]
    else:
        params = [TFloatI(expected_tfloati)]
    cursor.execute('INSERT INTO tbl_tfloati (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloati WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tfloati, tuple):
        assert result == TFloatI(*expected_tfloati)
    else:
        assert result == TFloatI(expected_tfloati)


@pytest.mark.parametrize('expected_tfloati', [
    '{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01}',
])
def test_tfloati_accessors(cursor, expected_tfloati):
    assert TFloatI(expected_tfloati).duration == TemporalDuration.InstantSet
    assert TFloatI(expected_tfloati).duration.name == 'InstantSet'
    assert TFloatI(expected_tfloati).getValues == {RangeFloat(10.0, 10.0, upper_inc=True),
                                             RangeFloat(20.0, 20.0, upper_inc=True),
                                             RangeFloat(30.0, 30.0, upper_inc=True)}
    assert TFloatI(expected_tfloati).startValue == 10.0
    assert TFloatI(expected_tfloati).endValue == 30.0
    assert TFloatI(expected_tfloati).minValue == 10.0
    assert TFloatI(expected_tfloati).maxValue == 30.0
    assert TFloatI(expected_tfloati).valueRange == floatrange(10.0, 30.0, upper_inc=True)
    assert TFloatI(expected_tfloati).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TFloatI(expected_tfloati).timespan == timedelta(0)
    assert TFloatI(expected_tfloati).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TFloatI(expected_tfloati).numInstants == 3
    assert TFloatI(expected_tfloati).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatI(expected_tfloati).endInstant == TFloatInst('30.0@2019-09-03 00:00:00+01')
    assert TFloatI(expected_tfloati).instantN(1) == TFloatInst('20.0@2019-09-02 00:00:00+01')
    assert TFloatI(expected_tfloati).instants == {TFloatInst('10.0@2019-09-01 00:00:00+01'),
                                            TFloatInst('20.0@2019-09-02 00:00:00+01'),
                                            TFloatInst('30.0@2019-09-03 00:00:00+01')}
    assert TFloatI(expected_tfloati).numTimestamps == 3
    assert TFloatI(expected_tfloati).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatI(expected_tfloati).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TFloatI(expected_tfloati).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TFloatI(expected_tfloati).timestamps == {parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                              parse('2019-09-03 00:00:00+01')}
    assert TFloatI(expected_tfloati).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatI(expected_tfloati).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TFloatI(expected_tfloati).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatI(expected_tfloati).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TFloatI(expected_tfloati).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatI(expected_tfloati).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TFloatI(expected_tfloati).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TFloatI(expected_tfloati).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatI(expected_tfloati).intersectsPeriodSet(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TFloatI(expected_tfloati).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tfloatseq', [
    '[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
    {'10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'},
    {TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
     TFloatInst('10.0@2019-09-03 00:00:00+01')},
    ({'10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'}, True, True,
     'Stepwise'),
    ({TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
      TFloatInst('10.0@2019-09-03 00:00:00+01')}, True, True, 'Stepwise'),
])
def test_tfloatseq_constructor(cursor, expected_tfloatseq):
    if isinstance(expected_tfloatseq, tuple):
        params = [TFloatSeq(*expected_tfloatseq)]
    else:
        params = [TFloatSeq(expected_tfloatseq)]
    cursor.execute('INSERT INTO tbl_tfloatseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tfloatseq, tuple):
        assert result == TFloatSeq(*expected_tfloatseq)
    else:
        assert result == TFloatSeq(expected_tfloatseq)


@pytest.mark.parametrize('expected_tfloatseq', [
    '[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]',
])
def test_tfloatseq_accessors(cursor, expected_tfloatseq):
    assert TFloatSeq(expected_tfloatseq).duration == TemporalDuration.Sequence
    assert TFloatSeq(expected_tfloatseq).duration.name == 'Sequence'
    assert TFloatSeq(expected_tfloatseq).getValues == {RangeFloat(10.0, 30.0, upper_inc=True)}
    assert TFloatSeq(expected_tfloatseq).startValue == 10.0
    assert TFloatSeq(expected_tfloatseq).endValue == 30.0
    assert TFloatSeq(expected_tfloatseq).minValue == 10.0
    assert TFloatSeq(expected_tfloatseq).maxValue == 30.0
    assert TFloatSeq(expected_tfloatseq).valueRange == floatrange(10.0, 30.0, upper_inc=True)
    assert TFloatSeq(expected_tfloatseq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TFloatSeq(expected_tfloatseq).timespan == timedelta(2)
    assert TFloatSeq(expected_tfloatseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TFloatSeq(expected_tfloatseq).numInstants == 3
    assert TFloatSeq(expected_tfloatseq).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatSeq(expected_tfloatseq).endInstant == TFloatInst('30.0@2019-09-03 00:00:00+01')
    assert TFloatSeq(expected_tfloatseq).instantN(1) == TFloatInst('20.0@2019-09-02 00:00:00+01')
    assert TFloatSeq(expected_tfloatseq).instants == \
           {TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
            TFloatInst('30.0@2019-09-03 00:00:00+01')}
    assert TFloatSeq(expected_tfloatseq).numTimestamps == 3
    assert TFloatSeq(expected_tfloatseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatSeq(expected_tfloatseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TFloatSeq(expected_tfloatseq).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TFloatSeq(expected_tfloatseq).timestamps == {parse('2019-09-01 00:00:00+01'),
                                                          parse('2019-09-02 00:00:00+01'),
                                                          parse('2019-09-03 00:00:00+01')}
    assert TFloatSeq(expected_tfloatseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatSeq(expected_tfloatseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TFloatSeq(expected_tfloatseq).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatSeq(expected_tfloatseq).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TFloatSeq(expected_tfloatseq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatSeq(expected_tfloatseq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TFloatSeq(expected_tfloatseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatSeq(expected_tfloatseq).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tfloats', [
    '{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
    # 'Interp=Stepwise;{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
    {'[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'},
    ({'[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'}, 'Linear'),
    # ({'Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'}, 'Stepwise'),
    {TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
     TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')},
    ({TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
      TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')}, 'Linear'),
    # ({TFloatSeq('Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]'),
    #   TFloatSeq('Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')}, 'Stepwise'),
])
def test_tfloats_constructor(cursor, expected_tfloats):
    if isinstance(expected_tfloats, tuple):
        params = [TFloatS(*expected_tfloats)]
    else:
        params = [TFloatS(expected_tfloats)]
    cursor.execute('INSERT INTO tbl_tfloats (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloats WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_tfloats, tuple):
        assert result == TFloatS(*expected_tfloats)
    else:
        assert result == TFloatS(expected_tfloats)


@pytest.mark.parametrize('expected_tfloats', [
    '{[10.0@2019-09-01 00:00:00+01],  [20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]}',
])
def test_tfloats_accessors(cursor, expected_tfloats):
    assert TFloatS(expected_tfloats).duration == TemporalDuration.SequenceSet
    assert TFloatS(expected_tfloats).duration.name == 'SequenceSet'
    assert TFloatS(expected_tfloats).getValues == {RangeFloat(10.0, 10.0, upper_inc=True), RangeFloat(20.0, 30.0, upper_inc=True)}
    assert TFloatS(expected_tfloats).startValue == 10.0
    assert TFloatS(expected_tfloats).endValue == 30.0
    assert TFloatS(expected_tfloats).minValue == 10.0
    assert TFloatS(expected_tfloats).maxValue == 30.0
    assert TFloatS(expected_tfloats).valueRange == floatrange(10.0, 30.0, upper_inc=True)
    assert TFloatS(expected_tfloats).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TFloatS(expected_tfloats).timespan == timedelta(1)
    assert TFloatS(expected_tfloats).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TFloatS(expected_tfloats).numInstants == 3
    assert TFloatS(expected_tfloats).startInstant == TFloatInst('10.0@2019-09-01 00:00:00+01')
    assert TFloatS(expected_tfloats).endInstant == TFloatInst('30.0@2019-09-03 00:00:00+01')
    assert TFloatS(expected_tfloats).instantN(1) == TFloatInst('20.0@2019-09-02 00:00:00+01')
    assert TFloatS(expected_tfloats).instants == {TFloatInst('10.0@2019-09-01 00:00:00+01'),
                                                    TFloatInst('20.0@2019-09-02 00:00:00+01'),
                                                    TFloatInst('30.0@2019-09-03 00:00:00+01')}
    assert TFloatS(expected_tfloats).numTimestamps == 3
    assert TFloatS(expected_tfloats).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TFloatS(expected_tfloats).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TFloatS(expected_tfloats).timestampN(1) == parse('2019-09-02 00:00:00+01')
    assert TFloatS(expected_tfloats).timestamps == {parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')}
    assert TFloatS(expected_tfloats).numSequences == 2
    assert TFloatS(expected_tfloats).startSequence == TFloatSeq('[10.0@2019-09-01 00:00:00+01]')
    assert TFloatS(expected_tfloats).endSequence == TFloatSeq(
        '[20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]')
    assert TFloatS(expected_tfloats).sequenceN(1) == TFloatSeq(
        '[20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]')
    assert TFloatS(expected_tfloats).sequences == {TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
                                                     TFloatSeq(
                                                         '[20.0@2019-09-02 00:00:00+01, 30.0@2019-09-03 00:00:00+01]')}
    assert TFloatS(expected_tfloats).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TFloatS(expected_tfloats).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TFloatS(expected_tfloats).intersectsTimestampSet(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TFloatS(expected_tfloats).intersectsTimestampSet(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TFloatS(expected_tfloats).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TFloatS(expected_tfloats).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TFloatS(expected_tfloats).intersectsPeriodSet(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TFloatS(expected_tfloats).intersectsPeriodSet(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
