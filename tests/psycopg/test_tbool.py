import pytest
from datetime import timedelta
from dateutil.parser import parse
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TBoolInst, TBoolI, TBoolSeq, TBoolS


@pytest.mark.parametrize('expected_tboolinst', [
	'true@2019-09-01 00:00:00+01',
	('true', '2019-09-08 00:00:00+01'),
	['true', '2019-09-08 00:00:00+01'],
	(True, '2019-09-08 00:00:00+01'),
	[True, parse('2019-09-08 00:00:00+01')],
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
	assert TBoolInst(expected_tboolinst).duration() == 'Instant'
	assert TBoolInst(expected_tboolinst).getValue() == True
	assert TBoolInst(expected_tboolinst).getValues() == [True]
	assert TBoolInst(expected_tboolinst).startValue() == True
	assert TBoolInst(expected_tboolinst).endValue() == True
	assert TBoolInst(expected_tboolinst).getTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).getTime() == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]}')
	assert TBoolInst(expected_tboolinst).timespan() == timedelta(0)
	assert TBoolInst(expected_tboolinst).period() == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
	assert TBoolInst(expected_tboolinst).numInstants() == 1
	assert TBoolInst(expected_tboolinst).startInstant() == TBoolInst('true@2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).endInstant() == TBoolInst('true@2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).instantN(1) == TBoolInst('true@2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).instants() == [TBoolInst('true@2019-09-01 00:00:00+01')]
	assert TBoolInst(expected_tboolinst).numTimestamps() == 1
	assert TBoolInst(expected_tboolinst).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).endTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).timestampN(1) == parse('2019-09-01 00:00:00+01')
	assert TBoolInst(expected_tboolinst).timestamps() == [parse('2019-09-01 00:00:00+01')]
	assert TBoolInst(expected_tboolinst).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TBoolInst(expected_tboolinst).intersectsTimestamp(parse('2019-09-02 00:00:00+01')) == False
	assert TBoolInst(expected_tboolinst).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TBoolInst(expected_tboolinst).intersectsTimestampset(
		TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}')) == False
	assert TBoolInst(expected_tboolinst).intersectsPeriod(
		Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TBoolInst(expected_tboolinst).intersectsPeriod(
		Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == False
	assert TBoolInst(expected_tboolinst).intersectsPeriod(
		Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')) == False
	assert TBoolInst(expected_tboolinst).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TBoolInst(expected_tboolinst).intersectsPeriodset(
		PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == False
	assert TBoolInst(expected_tboolinst).intersectsPeriodset(
		PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')) == False

@pytest.mark.parametrize('expected_tbooli', [
	'{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
	('true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'),
	(TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	 TBoolInst('true@2019-09-03 00:00:00+01')),
	['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'],
	[TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	 TBoolInst('true@2019-09-03 00:00:00+01')],
])
def test_tbooli_constructor(cursor, expected_tbooli):
	if isinstance(expected_tbooli, tuple):
		params = [TBoolI(*expected_tbooli)]
	else:
		params = [TBoolI(expected_tbooli)]
	cursor.execute('INSERT INTO tbl_tbooli (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tbooli WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	if isinstance(expected_tbooli, tuple):
		assert result == TBoolI(*expected_tbooli)
	else:
		assert result == TBoolI(expected_tbooli)

@pytest.mark.parametrize('expected_tbooli', [
	'{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
])
def test_tbooli_accessors(cursor, expected_tbooli):
	assert TBoolI(expected_tbooli).duration() == 'InstantSet'
	assert TBoolI(expected_tbooli).getValues() == [True, False]
	assert TBoolI(expected_tbooli).startValue() == True
	assert TBoolI(expected_tbooli).endValue() == True
	assert TBoolI(expected_tbooli).getTime() == \
		   PeriodSet(
			   '{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01], [2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01], '
			   '[2019-09-03 00:00:00+01, 2019-09-03 00:00:00+01]}')
	assert TBoolI(expected_tbooli).timespan() == timedelta(2)
	assert TBoolI(expected_tbooli).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TBoolI(expected_tbooli).numInstants() == 3
	assert TBoolI(expected_tbooli).startInstant() == TBoolInst('true@2019-09-01 00:00:00+01')
	assert TBoolI(expected_tbooli).endInstant() == TBoolInst('true@2019-09-03 00:00:00+01')
	assert TBoolI(expected_tbooli).instantN(2) == TBoolInst('false@2019-09-02 00:00:00+01')
	assert TBoolI(expected_tbooli).instants() == [TBoolInst('true@2019-09-01 00:00:00+01'),
												TBoolInst('false@2019-09-02 00:00:00+01'),
												TBoolInst('true@2019-09-03 00:00:00+01')]
	assert TBoolI(expected_tbooli).numTimestamps() == 3
	assert TBoolI(expected_tbooli).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TBoolI(expected_tbooli).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TBoolI(expected_tbooli).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TBoolI(expected_tbooli).timestamps() == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
												  parse('2019-09-03 00:00:00+01')]
	assert TBoolI(expected_tbooli).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TBoolI(expected_tbooli).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
	assert TBoolI(expected_tbooli).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TBoolI(expected_tbooli).intersectsTimestampset(
		TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
	assert TBoolI(expected_tbooli).intersectsPeriod(Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TBoolI(expected_tbooli).intersectsPeriod(Period('(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)')) == False
	assert TBoolI(expected_tbooli).intersectsPeriod(Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
	assert TBoolI(expected_tbooli).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TBoolI(expected_tbooli).intersectsPeriodset(
		PeriodSet('{(2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01)}')) == False
	assert TBoolI(expected_tbooli).intersectsPeriodset(
		PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False

@pytest.mark.parametrize('expected_tboolseq', [
	'[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, false@2019-09-03 00:00:00+01]',
	'Interp=Stepwise;[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, false@2019-09-03 00:00:00+01]',
	['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'false@2019-09-03 00:00:00+01'],
	[TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	 TBoolInst('false@2019-09-03 00:00:00+01')],
	(['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'], True, True),
	([TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
	  TBoolInst('true@2019-09-03 00:00:00+01')], True, True),
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
	assert TBoolSeq(expected_tboolseq).duration() == 'Sequence'
	assert TBoolSeq(expected_tboolseq).getValues() == [True, False]
	assert TBoolSeq(expected_tboolseq).startValue() == True
	assert TBoolSeq(expected_tboolseq).endValue() == True
	assert TBoolSeq(expected_tboolseq).getTime() == PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]}')
	assert TBoolSeq(expected_tboolseq).timespan() == timedelta(2)
	assert TBoolSeq(expected_tboolseq).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TBoolSeq(expected_tboolseq).numInstants() == 3
	assert TBoolSeq(expected_tboolseq).startInstant() == TBoolInst('true@2019-09-01 00:00:00+01')
	assert TBoolSeq(expected_tboolseq).endInstant() == TBoolInst('true@2019-09-03 00:00:00+01')
	assert TBoolSeq(expected_tboolseq).instantN(2) == TBoolInst('false@2019-09-02 00:00:00+01')
	assert TBoolSeq(expected_tboolseq).instants() == \
		   [TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
			TBoolInst('true@2019-09-03 00:00:00+01')]
	assert TBoolSeq(expected_tboolseq).numTimestamps() == 3
	assert TBoolSeq(expected_tboolseq).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TBoolSeq(expected_tboolseq).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TBoolSeq(expected_tboolseq).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TBoolSeq(expected_tboolseq).timestamps() == [parse('2019-09-01 00:00:00+01'),
													  parse('2019-09-02 00:00:00+01'),
													  parse('2019-09-03 00:00:00+01')]
	assert TBoolSeq(expected_tboolseq).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TBoolSeq(expected_tboolseq).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
	assert TBoolSeq(expected_tboolseq).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TBoolSeq(expected_tboolseq).intersectsTimestampset(
		TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
	assert TBoolSeq(expected_tboolseq).intersectsPeriod(
		Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TBoolSeq(expected_tboolseq).intersectsPeriod(
		Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
	assert TBoolSeq(expected_tboolseq).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TBoolSeq(expected_tboolseq).intersectsPeriodset(
		PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False


@pytest.mark.parametrize('expected_tbools', [
	'{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
	'Interp=Stepwise;{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
	['[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'],
	[TBoolSeq('[true@2019-09-01 00:00:00+01]'),
	 TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')],
])
def test_tbools_constructor(cursor, expected_tbools):
	if isinstance(expected_tbools, tuple):
		params = [TBoolS(*expected_tbools)]
	else:
		params = [TBoolS(expected_tbools)]
	cursor.execute('INSERT INTO tbl_tbools (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tbools WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	if isinstance(expected_tbools, tuple):
		assert result == TBoolS(*expected_tbools)
	else:
		assert result == TBoolS(expected_tbools)


@pytest.mark.parametrize('expected_tbools', [
	'{[true@2019-09-01 00:00:00+01],  [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
])
def test_tbools_accessors(cursor, expected_tbools):
	assert TBoolS(expected_tbools).duration() == 'SequenceSet'
	assert TBoolS(expected_tbools).getValues() == [True, False]
	assert TBoolS(expected_tbools).startValue() == True
	assert TBoolS(expected_tbools).endValue() == True
	assert TBoolS(expected_tbools).getTime() == PeriodSet(
		'{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}')
	assert TBoolS(expected_tbools).timespan() == timedelta(2)
	assert TBoolS(expected_tbools).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TBoolS(expected_tbools).numInstants() == 3
	assert TBoolS(expected_tbools).startInstant() == TBoolInst('true@2019-09-01 00:00:00+01')
	assert TBoolS(expected_tbools).endInstant() == TBoolInst('true@2019-09-03 00:00:00+01')
	assert TBoolS(expected_tbools).instantN(2) == TBoolInst('false@2019-09-02 00:00:00+01')
	assert TBoolS(expected_tbools).instants() == [TBoolInst('true@2019-09-01 00:00:00+01'),
												TBoolInst('false@2019-09-02 00:00:00+01'),
												TBoolInst('true@2019-09-03 00:00:00+01')]
	assert TBoolS(expected_tbools).numTimestamps() == 3
	assert TBoolS(expected_tbools).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TBoolS(expected_tbools).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TBoolS(expected_tbools).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TBoolS(expected_tbools).timestamps() == [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'),
												  parse('2019-09-03 00:00:00+01')]
	assert TBoolS(expected_tbools).numSequences() == 2
	assert TBoolS(expected_tbools).startSequence() == TBoolSeq('[true@2019-09-01 00:00:00+01]')
	assert TBoolS(expected_tbools).endSequence() == TBoolSeq(
		'[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')
	assert TBoolS(expected_tbools).sequenceN(2) == TBoolSeq(
		'[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')
	assert TBoolS(expected_tbools).sequences() == [TBoolSeq('[true@2019-09-01 00:00:00+01]'),
												 TBoolSeq(
													 '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')]
	assert TBoolS(expected_tbools).intersectsTimestamp(parse('2019-09-01 00:00:00+01')) == True
	assert TBoolS(expected_tbools).intersectsTimestamp(parse('2019-09-04 00:00:00+01')) == False
	assert TBoolS(expected_tbools).intersectsTimestampset(
		TimestampSet('{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01}')) == True
	assert TBoolS(expected_tbools).intersectsTimestampset(
		TimestampSet('{2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01}')) == False
	assert TBoolS(expected_tbools).intersectsPeriod(
		Period('[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]')) == True
	assert TBoolS(expected_tbools).intersectsPeriod(
		Period('[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]')) == False
	assert TBoolS(expected_tbools).intersectsPeriodset(
		PeriodSet('{[2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01]}')) == True
	assert TBoolS(expected_tbools).intersectsPeriodset(
		PeriodSet('{[2019-09-04 00:00:00+01, 2019-09-05 00:00:00+01]}')) == False
