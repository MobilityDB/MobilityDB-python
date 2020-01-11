import pytest
from datetime import timedelta
from dateutil.parser import parse
from mobilitydb.main import TTextInst, TTextI, TTextSeq, TTextS
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
    assert TTextInst(expected_ttextinst).duration() == 'Instant'
    assert TTextInst(expected_ttextinst).getValue == 'AA'
    assert TTextInst(expected_ttextinst).getValues == ['AA']
    assert TTextInst(expected_ttextinst).startValue == 'AA'
    assert TTextInst(expected_ttextinst).endValue == 'AA'
    assert TTextInst(expected_ttextinst).minValue == 'AA'
    assert TTextInst(expected_ttextinst).maxValue == 'AA'
    assert TTextInst(expected_ttextinst).getTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextInst(expected_ttextinst).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
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
    assert TTextInst(expected_ttextinst).intersectsTimestampset(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextInst(expected_ttextinst).intersectsTimestampset(
        TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextInst(expected_ttextinst).intersectsPeriod(
        Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriod(
        Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriodset(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextInst(expected_ttextinst).intersectsPeriodset(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
    assert TTextInst(expected_ttextinst).intersectsPeriodset(
        PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False

@pytest.mark.parametrize('expected_ttexti', [
    '{AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01}',
    ('AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'),
    (TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('AA@2019-09-03 00:00:00+01')),
    ['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'],
    [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('AA@2019-09-03 00:00:00+01')],
])
def test_ttexti_constructor(cursor, expected_ttexti):
    if isinstance(expected_ttexti, tuple):
        params = [TTextI(*expected_ttexti)]
    else:
        params = [TTextI(expected_ttexti)]
    cursor.execute('INSERT INTO tbl_ttexti (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttexti WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_ttexti, tuple):
        assert result == TTextI(*expected_ttexti)
    else:
        assert result == TTextI(expected_ttexti)


@pytest.mark.parametrize('expected_ttexti', [
    '{AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01}',
])
def test_ttexti_accessors(cursor, expected_ttexti):
    assert TTextI(expected_ttexti).duration() == 'InstantSet'
    assert TTextI(expected_ttexti).getValues == ['AA', 'BB', 'CC']
    assert TTextI(expected_ttexti).startValue == 'AA'
    assert TTextI(expected_ttexti).endValue == 'CC'
    assert TTextI(expected_ttexti).minValue == 'AA'
    assert TTextI(expected_ttexti).maxValue == 'CC'
    assert TTextI(expected_ttexti).getTime == \
           PeriodSet(
               '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
               '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TTextI(expected_ttexti).timespan == timedelta(0)
    assert TTextI(expected_ttexti).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TTextI(expected_ttexti).numInstants == 3
    assert TTextI(expected_ttexti).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextI(expected_ttexti).endInstant == TTextInst('CC@2019-09-03 00:00:00+01')
    assert TTextI(expected_ttexti).instantN(2) == TTextInst('BB@2019-09-02 00:00:00+01')
    assert TTextI(expected_ttexti).instants == [TTextInst('AA@2019-09-01 00:00:00+01'),
                                                TTextInst('BB@2019-09-02 00:00:00+01'),
                                                TTextInst('CC@2019-09-03 00:00:00+01')]
    assert TTextI(expected_ttexti).numTimestamps == 3
    assert TTextI(expected_ttexti).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextI(expected_ttexti).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TTextI(expected_ttexti).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TTextI(expected_ttexti).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')]
    assert TTextI(expected_ttexti).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextI(expected_ttexti).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TTextI(expected_ttexti).intersectsTimestampset(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextI(expected_ttexti).intersectsTimestampset(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TTextI(expected_ttexti).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextI(expected_ttexti).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
    assert TTextI(expected_ttexti).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TTextI(expected_ttexti).intersectsPeriodset(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextI(expected_ttexti).intersectsPeriodset(
        PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
    assert TTextI(expected_ttexti).intersectsPeriodset(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_ttextseq', [
    '[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, BB@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, BB@2019-09-03 00:00:00+01]',
    ['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'BB@2019-09-03 00:00:00+01'],
    [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
     TTextInst('BB@2019-09-03 00:00:00+01')],
    (['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'], True, True),
    ([TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
      TTextInst('AA@2019-09-03 00:00:00+01')], True, True),
])
def test_ttextseq_constructor(cursor, expected_ttextseq):
    if isinstance(expected_ttextseq, tuple):
        params = [TTextSeq(*expected_ttextseq)]
    else:
        params = [TTextSeq(expected_ttextseq)]
    cursor.execute('INSERT INTO tbl_ttextseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttextseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_ttextseq, tuple):
        assert result == TTextSeq(*expected_ttextseq)
    else:
        assert result == TTextSeq(expected_ttextseq)


@pytest.mark.parametrize('expected_ttextseq', [
    '[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]',
])
def test_ttextseq_accessors(cursor, expected_ttextseq):
    assert TTextSeq(expected_ttextseq).duration() == 'Sequence'
    assert TTextSeq(expected_ttextseq).getValues == ['AA', 'BB', 'CC']
    assert TTextSeq(expected_ttextseq).startValue == 'AA'
    assert TTextSeq(expected_ttextseq).endValue == 'CC'
    assert TTextSeq(expected_ttextseq).minValue == 'AA'
    assert TTextSeq(expected_ttextseq).maxValue == 'CC'
    assert TTextSeq(expected_ttextseq).getTime == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TTextSeq(expected_ttextseq).timespan == timedelta(2)
    assert TTextSeq(expected_ttextseq).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TTextSeq(expected_ttextseq).numInstants == 3
    assert TTextSeq(expected_ttextseq).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextSeq(expected_ttextseq).endInstant == TTextInst('CC@2019-09-03 00:00:00+01')
    assert TTextSeq(expected_ttextseq).instantN(2) == TTextInst('BB@2019-09-02 00:00:00+01')
    assert TTextSeq(expected_ttextseq).instants == \
           [TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'),
            TTextInst('CC@2019-09-03 00:00:00+01')]
    assert TTextSeq(expected_ttextseq).numTimestamps == 3
    assert TTextSeq(expected_ttextseq).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextSeq(expected_ttextseq).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TTextSeq(expected_ttextseq).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TTextSeq(expected_ttextseq).timestamps == [parse('2019-09-01 00:00:00+01'),
                                                      parse('2019-09-02 00:00:00+01'),
                                                      parse('2019-09-03 00:00:00+01')]
    assert TTextSeq(expected_ttextseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextSeq(expected_ttextseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TTextSeq(expected_ttextseq).intersectsTimestampset(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextSeq(expected_ttextseq).intersectsTimestampset(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TTextSeq(expected_ttextseq).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextSeq(expected_ttextseq).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TTextSeq(expected_ttextseq).intersectsPeriodset(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextSeq(expected_ttextseq).intersectsPeriodset(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_ttexts', [
    '{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}',
    'Interp=Stepwise;{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}',
    ['[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'],
    [TTextSeq('[AA@2019-09-01 00:00:00+01]'),
     TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')],
])
def test_ttexts_constructor(cursor, expected_ttexts):
    if isinstance(expected_ttexts, tuple):
        params = [TTextS(*expected_ttexts)]
    else:
        params = [TTextS(expected_ttexts)]
    cursor.execute('INSERT INTO tbl_ttexts (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_ttexts WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    if isinstance(expected_ttexts, tuple):
        assert result == TTextS(*expected_ttexts)
    else:
        assert result == TTextS(expected_ttexts)


@pytest.mark.parametrize('expected_ttexts', [
    '{[AA@2019-09-01 00:00:00+01],  [BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]}',
])
def test_ttexts_accessors(cursor, expected_ttexts):
    assert TTextS(expected_ttexts).duration() == 'SequenceSet'
    assert TTextS(expected_ttexts).getValues == ['AA', 'BB', 'CC']
    assert TTextS(expected_ttexts).startValue == 'AA'
    assert TTextS(expected_ttexts).endValue == 'CC'
    assert TTextS(expected_ttexts).minValue == 'AA'
    assert TTextS(expected_ttexts).maxValue == 'CC'
    assert TTextS(expected_ttexts).getTime == PeriodSet(
        '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
    assert TTextS(expected_ttexts).timespan == timedelta(1)
    assert TTextS(expected_ttexts).period == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
    assert TTextS(expected_ttexts).numInstants == 3
    assert TTextS(expected_ttexts).startInstant == TTextInst('AA@2019-09-01 00:00:00+01')
    assert TTextS(expected_ttexts).endInstant == TTextInst('CC@2019-09-03 00:00:00+01')
    assert TTextS(expected_ttexts).instantN(2) == TTextInst('BB@2019-09-02 00:00:00+01')
    assert TTextS(expected_ttexts).instants == [TTextInst('AA@2019-09-01 00:00:00+01'),
                                                TTextInst('BB@2019-09-02 00:00:00+01'),
                                                TTextInst('CC@2019-09-03 00:00:00+01')]
    assert TTextS(expected_ttexts).numTimestamps == 3
    assert TTextS(expected_ttexts).startTimestamp == parse('2019-09-01 00:00:00+01')
    assert TTextS(expected_ttexts).endTimestamp == parse('2019-09-03 00:00:00+01')
    assert TTextS(expected_ttexts).timestampN(2) == parse('2019-09-02 00:00:00+01')
    assert TTextS(expected_ttexts).timestamps == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
                                                  parse('2019-09-03 00:00:00+01')]
    assert TTextS(expected_ttexts).numSequences == 2
    assert TTextS(expected_ttexts).startSequence == TTextSeq('[AA@2019-09-01 00:00:00+01]')
    assert TTextS(expected_ttexts).endSequence == TTextSeq(
        '[BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]')
    assert TTextS(expected_ttexts).sequenceN(2) == TTextSeq(
        '[BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]')
    assert TTextS(expected_ttexts).sequences == [TTextSeq('[AA@2019-09-01 00:00:00+01]'),
                                                 TTextSeq(
                                                     '[BB@2019-09-02 00:00:00+01, CC@2019-09-03 00:00:00+01]')]
    assert TTextS(expected_ttexts).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
    assert TTextS(expected_ttexts).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
    assert TTextS(expected_ttexts).intersectsTimestampset(
        TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
    assert TTextS(expected_ttexts).intersectsTimestampset(
        TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
    assert TTextS(expected_ttexts).intersectsPeriod(
        Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
    assert TTextS(expected_ttexts).intersectsPeriod(
        Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
    assert TTextS(expected_ttexts).intersectsPeriodset(
        PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
    assert TTextS(expected_ttexts).intersectsPeriodset(
        PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
