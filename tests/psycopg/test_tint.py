import pytest
from datetime import timedelta
from dateutil.parser import parse
from spans.types import intrange
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TIntInst, TIntI, TIntSeq, TIntS


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
	assert TIntInst(expected_tintinst).duration() == 'Instant'
	assert TIntInst(expected_tintinst).getValue() == 10
	assert TIntInst(expected_tintinst).getValues() == [10]
	assert TIntInst(expected_tintinst).startValue() == 10
	assert TIntInst(expected_tintinst).endValue() == 10
	assert TIntInst(expected_tintinst).minValue() == 10
	assert TIntInst(expected_tintinst).maxValue() == 10
	assert TIntInst(expected_tintinst).valueRange() == intrange(10, 10, upper_inc=True)
	assert TIntInst(expected_tintinst).getTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).getTime() == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
	assert TIntInst(expected_tintinst).timespan() == timedelta(0)
	assert TIntInst(expected_tintinst).period() == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
	assert TIntInst(expected_tintinst).numInstants() == 1
	assert TIntInst(expected_tintinst).startInstant() == TIntInst('10@2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).endInstant() == TIntInst('10@2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).instantN(1) == TIntInst('10@2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).instants() == [TIntInst('10@2019-09-01 00:00:00+01')]
	assert TIntInst(expected_tintinst).numTimestamps() == 1
	assert TIntInst(expected_tintinst).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).endTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).timestampN(1) == parse('2019-09-01 00:00:00+01')
	assert TIntInst(expected_tintinst).timestamps() == [parse('2019-09-01 00:00:00+01')]
	assert TIntInst(expected_tintinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TIntInst(expected_tintinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
	assert TIntInst(expected_tintinst).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TIntInst(expected_tintinst).intersectsTimestampset(
		TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
	assert TIntInst(expected_tintinst).intersectsPeriod(
		Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TIntInst(expected_tintinst).intersectsPeriod(
		Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
	assert TIntInst(expected_tintinst).intersectsPeriod(
		Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
	assert TIntInst(expected_tintinst).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TIntInst(expected_tintinst).intersectsPeriodset(
		PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
	assert TIntInst(expected_tintinst).intersectsPeriodset(
		PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tinti', [
	'{10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01}',
	('10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'),
	(TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
	 TIntInst('10@2019-09-03 00:00:00+01')),
	['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'],
	[TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
	 TIntInst('10@2019-09-03 00:00:00+01')],
])
def test_tinti_constructor(cursor, expected_tinti):
	if isinstance(expected_tinti, tuple):
		params = [TIntI(*expected_tinti)]
	else:
		params = [TIntI(expected_tinti)]
	cursor.execute('INSERT INTO tbl_tinti (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tinti WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	if isinstance(expected_tinti, tuple):
		assert result == TIntI(*expected_tinti)
	else:
		assert result == TIntI(expected_tinti)


@pytest.mark.parametrize('expected_tinti', [
	'{10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01}',
])
def test_tinti_accessors(cursor, expected_tinti):
	assert TIntI(expected_tinti).duration() == 'InstantSet'
	assert TIntI(expected_tinti).getValues() == [10, 20, 30]
	assert TIntI(expected_tinti).startValue() == 10
	assert TIntI(expected_tinti).endValue() == 30
	assert TIntI(expected_tinti).minValue() == 10
	assert TIntI(expected_tinti).maxValue() == 30
	assert TIntI(expected_tinti).valueRange() == intrange(10, 30, upper_inc=True)
	assert TIntI(expected_tinti).getTime() == \
		   PeriodSet(
			   '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
			   '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
	assert TIntI(expected_tinti).timespan() == timedelta(2)
	assert TIntI(expected_tinti).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TIntI(expected_tinti).numInstants() == 3
	assert TIntI(expected_tinti).startInstant() == TIntInst('10@2019-09-01 00:00:00+01')
	assert TIntI(expected_tinti).endInstant() == TIntInst('30@2019-09-03 00:00:00+01')
	assert TIntI(expected_tinti).instantN(2) == TIntInst('20@2019-09-02 00:00:00+01')
	assert TIntI(expected_tinti).instants() == [TIntInst('10@2019-09-01 00:00:00+01'),
												TIntInst('20@2019-09-02 00:00:00+01'),
												TIntInst('30@2019-09-03 00:00:00+01')]
	assert TIntI(expected_tinti).numTimestamps() == 3
	assert TIntI(expected_tinti).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TIntI(expected_tinti).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TIntI(expected_tinti).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TIntI(expected_tinti).timestamps() == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
												  parse('2019-09-03 00:00:00+01')]
	assert TIntI(expected_tinti).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TIntI(expected_tinti).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
	assert TIntI(expected_tinti).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TIntI(expected_tinti).intersectsTimestampset(
		TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
	assert TIntI(expected_tinti).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TIntI(expected_tinti).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
	assert TIntI(expected_tinti).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
	assert TIntI(expected_tinti).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TIntI(expected_tinti).intersectsPeriodset(
		PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
	assert TIntI(expected_tinti).intersectsPeriodset(
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
	assert TIntSeq(expected_tintseq).duration() == 'Sequence'
	assert TIntSeq(expected_tintseq).getValues() == [10, 20, 30]
	assert TIntSeq(expected_tintseq).startValue() == 10
	assert TIntSeq(expected_tintseq).endValue() == 30
	assert TIntSeq(expected_tintseq).minValue() == 10
	assert TIntSeq(expected_tintseq).maxValue() == 30
	assert TIntSeq(expected_tintseq).valueRange() == intrange(10, 30, upper_inc=True)
	assert TIntSeq(expected_tintseq).getTime() == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
	assert TIntSeq(expected_tintseq).timespan() == timedelta(2)
	assert TIntSeq(expected_tintseq).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TIntSeq(expected_tintseq).numInstants() == 3
	assert TIntSeq(expected_tintseq).startInstant() == TIntInst('10@2019-09-01 00:00:00+01')
	assert TIntSeq(expected_tintseq).endInstant() == TIntInst('30@2019-09-03 00:00:00+01')
	assert TIntSeq(expected_tintseq).instantN(2) == TIntInst('20@2019-09-02 00:00:00+01')
	assert TIntSeq(expected_tintseq).instants() == \
		   [TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'),
			TIntInst('30@2019-09-03 00:00:00+01')]
	assert TIntSeq(expected_tintseq).numTimestamps() == 3
	assert TIntSeq(expected_tintseq).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TIntSeq(expected_tintseq).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TIntSeq(expected_tintseq).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TIntSeq(expected_tintseq).timestamps() == [parse('2019-09-01 00:00:00+01'),
													  parse('2019-09-02 00:00:00+01'),
													  parse('2019-09-03 00:00:00+01')]
	assert TIntSeq(expected_tintseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TIntSeq(expected_tintseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
	assert TIntSeq(expected_tintseq).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TIntSeq(expected_tintseq).intersectsTimestampset(
		TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
	assert TIntSeq(expected_tintseq).intersectsPeriod(
		Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TIntSeq(expected_tintseq).intersectsPeriod(
		Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
	assert TIntSeq(expected_tintseq).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TIntSeq(expected_tintseq).intersectsPeriodset(
		PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tints', [
	'{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}',
	'Interp=Stepwise;{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}',
	['[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'],
	[TIntSeq('[10@2019-09-01 00:00:00+01]'),
	 TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')],
])
def test_tints_constructor(cursor, expected_tints):
	if isinstance(expected_tints, tuple):
		params = [TIntS(*expected_tints)]
	else:
		params = [TIntS(expected_tints)]
	cursor.execute('INSERT INTO tbl_tints (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tints WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	if isinstance(expected_tints, tuple):
		assert result == TIntS(*expected_tints)
	else:
		assert result == TIntS(expected_tints)


@pytest.mark.parametrize('expected_tints', [
	'{[10@2019-09-01 00:00:00+01],  [20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]}',
])
def test_tints_accessors(cursor, expected_tints):
	assert TIntS(expected_tints).duration() == 'SequenceSet'
	assert TIntS(expected_tints).getValues() == [10, 20, 30]
	assert TIntS(expected_tints).startValue() == 10
	assert TIntS(expected_tints).endValue() == 30
	assert TIntS(expected_tints).minValue() == 10
	assert TIntS(expected_tints).maxValue() == 30
	assert TIntS(expected_tints).valueRange() == intrange(10, 30, upper_inc=True)
	assert TIntS(expected_tints).getTime() == PeriodSet(
		'{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
	assert TIntS(expected_tints).timespan() == timedelta(2)
	assert TIntS(expected_tints).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TIntS(expected_tints).numInstants() == 3
	assert TIntS(expected_tints).startInstant() == TIntInst('10@2019-09-01 00:00:00+01')
	assert TIntS(expected_tints).endInstant() == TIntInst('30@2019-09-03 00:00:00+01')
	assert TIntS(expected_tints).instantN(2) == TIntInst('20@2019-09-02 00:00:00+01')
	assert TIntS(expected_tints).instants() == [TIntInst('10@2019-09-01 00:00:00+01'),
												TIntInst('20@2019-09-02 00:00:00+01'),
												TIntInst('30@2019-09-03 00:00:00+01')]
	assert TIntS(expected_tints).numTimestamps() == 3
	assert TIntS(expected_tints).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TIntS(expected_tints).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TIntS(expected_tints).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TIntS(expected_tints).timestamps() == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
												  parse('2019-09-03 00:00:00+01')]
	assert TIntS(expected_tints).numSequences() == 2
	assert TIntS(expected_tints).startSequence() == TIntSeq('[10@2019-09-01 00:00:00+01]')
	assert TIntS(expected_tints).endSequence() == TIntSeq(
		'[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')
	assert TIntS(expected_tints).sequenceN(2) == TIntSeq(
		'[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')
	assert TIntS(expected_tints).sequences() == [TIntSeq('[10@2019-09-01 00:00:00+01]'),
												 TIntSeq(
													 '[20@2019-09-02 00:00:00+01, 30@2019-09-03 00:00:00+01]')]
	assert TIntS(expected_tints).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TIntS(expected_tints).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
	assert TIntS(expected_tints).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TIntS(expected_tints).intersectsTimestampset(
		TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
	assert TIntS(expected_tints).intersectsPeriod(
		Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TIntS(expected_tints).intersectsPeriod(
		Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
	assert TIntS(expected_tints).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TIntS(expected_tints).intersectsPeriodset(
		PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
