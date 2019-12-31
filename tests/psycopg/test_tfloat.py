import pytest
from datetime import datetime, timedelta
from dateutil.tz import tzoffset
from bdateutil.parser import parse
from spans.types import Range
from MobilityDB.MainTypes import TFloatInst, TFloatI, TFloatSeq, TFloatS
from MobilityDB.TimeTypes import TimestampSet, Period, PeriodSet


class floatrange(Range):
	__slots__ = ()
	type = float


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

@pytest.mark.parametrize('expected', [
	'10.0@2019-09-01 00:00:00',
	#'10.0@2019-09-01 00:00:00+01',
])
def test_tfloatinst_accessors(cursor, expected):
	assert TFloatInst(expected).duration() == 'Instant'
	assert TFloatInst(expected).getValue() == 10.0
	#assert TFloatInst(expected).getValues() == floatrange(10.0, 10.0, upper_inc=True)
	assert TFloatInst(expected).startValue() == 10.0
	assert TFloatInst(expected).endValue() == 10.0
	assert TFloatInst(expected).minValue() == 10.0
	assert TFloatInst(expected).maxValue() == 10.0
	#assert TFloatInst(expected).valueRange() == floatrange(10.0, 10.0, upper_inc=True)
	assert TFloatInst(expected).getTimestamp() == parse('2019-09-01 00:00:00')
	assert TFloatInst(expected).getTime() == PeriodSet('{[2019-09-01 00:00:00, 2019-09-01 00:00:00]}')
	assert TFloatInst(expected).timespan() == timedelta(0)
	assert TFloatInst(expected).period() == Period('[2019-09-01 00:00:00, 2019-09-01 00:00:00]')
	assert TFloatInst(expected).numInstants() == 1
	assert TFloatInst(expected).startInstant() == TFloatInst('10.0@2019-09-01 00:00:00')
	assert TFloatInst(expected).endInstant() == TFloatInst('10.0@2019-09-01 00:00:00')
	assert TFloatInst(expected).instantN(1) == TFloatInst('10.0@2019-09-01 00:00:00')
	assert TFloatInst(expected).instants() == [TFloatInst('10.0@2019-09-01 00:00:00')]
	assert TFloatInst(expected).numTimestamps() == 1
	assert TFloatInst(expected).startTimestamp() == parse('2019-09-01 00:00:00')
	assert TFloatInst(expected).endTimestamp() == parse('2019-09-01 00:00:00')
	assert TFloatInst(expected).timestampN(1) == parse('2019-09-01 00:00:00')
	assert TFloatInst(expected).timestamps() == [parse('2019-09-01 00:00:00')]
	assert TFloatInst(expected).intersectsTimestamp(parse('2019-09-01 00:00:00')) == True
	assert TFloatInst(expected).intersectsTimestamp(parse('2019-09-02 00:00:00')) == False
	assert TFloatInst(expected).intersectsTimestampset(TimestampSet('{2019-09-01 00:00:00, 2019-09-02 00:00:00}')) == True
	assert TFloatInst(expected).intersectsTimestampset(TimestampSet('{2019-09-02 00:00:00, 2019-09-03 00:00:00}')) == False
	assert TFloatInst(expected).intersectsPeriod(Period('[2019-09-01 00:00:00, 2019-09-02 00:00:00]')) == True
	assert TFloatInst(expected).intersectsPeriod(Period('(2019-09-01 00:00:00, 2019-09-02 00:00:00]')) == False
	assert TFloatInst(expected).intersectsPeriod(Period('[2019-09-02 00:00:00, 2019-09-03 00:00:00]')) == False
	assert TFloatInst(expected).intersectsPeriodset(PeriodSet('{[2019-09-01 00:00:00, 2019-09-02 00:00:00]}')) == True
	assert TFloatInst(expected).intersectsPeriodset(PeriodSet('{(2019-09-01 00:00:00, 2019-09-02 00:00:00]}')) == False
	assert TFloatInst(expected).intersectsPeriodset(PeriodSet('{[2019-09-02 00:00:00, 2019-09-03 00:00:00]}')) == False


@pytest.mark.parametrize('expected', [
	'{10.0@2019-09-01 00:00:00, 20.0@2019-09-02 00:00:00, 30.0@2019-09-03 00:00:00}',
	#'10.0@2019-09-01 00:00:00+01',
])
def test_TFloatI_accessors(cursor, expected):
	assert TFloatI(expected).duration() == 'InstantSet'
	#assert TFloatI(expected).getValues() == [floatrange(10.0, 10.0, upper_inc=True),floatrange(20.0, 20.0, upper_inc=True),floatrange(30.0, 30.0, upper_inc=True)]
	assert TFloatI(expected).startValue() == 10.0
	assert TFloatI(expected).endValue() == 30.0
	assert TFloatI(expected).minValue() == 10.0
	assert TFloatI(expected).maxValue() == 30.0
	#assert TFloatI(expected).valueRange() == floatrange(10.0, 30.0, upper_inc=True)
	assert TFloatI(expected).getTime() == PeriodSet('{[2019-09-01 00:00:00, 2019-09-01 00:00:00], [2019-09-02 00:00:00, 2019-09-02 00:00:00], [2019-09-03 00:00:00, 2019-09-03 00:00:00]}')
	assert TFloatI(expected).timespan() == timedelta(2)
	assert TFloatI(expected).period() == Period('[2019-09-01 00:00:00, 2019-09-03 00:00:00]')
	assert TFloatI(expected).numInstants() == 3
	assert TFloatI(expected).startInstant() == TFloatInst('10.0@2019-09-01 00:00:00')
	assert TFloatI(expected).endInstant() == TFloatInst('30.0@2019-09-03 00:00:00')
	assert TFloatI(expected).instantN(2) == TFloatInst('20.0@2019-09-02 00:00:00')
	assert TFloatI(expected).instants() == [TFloatInst('10.0@2019-09-01 00:00:00'), TFloatInst('20.0@2019-09-02 00:00:00'), TFloatInst('30.0@2019-09-03 00:00:00')]
	assert TFloatI(expected).numTimestamps() == 3
	assert TFloatI(expected).startTimestamp() == parse('2019-09-01 00:00:00')
	assert TFloatI(expected).endTimestamp() == parse('2019-09-03 00:00:00')
	assert TFloatI(expected).timestampN(2) == parse('2019-09-02 00:00:00')
	assert TFloatI(expected).timestamps() == [parse('2019-09-01 00:00:00'), parse('2019-09-02 00:00:00'), parse('2019-09-03 00:00:00')]
	assert TFloatI(expected).intersectsTimestamp(parse('2019-09-01 00:00:00')) == True
	assert TFloatI(expected).intersectsTimestamp(parse('2019-09-04 00:00:00')) == False
	assert TFloatI(expected).intersectsTimestampset(TimestampSet('{2019-09-01 00:00:00, 2019-09-02 00:00:00}')) == True
	assert TFloatI(expected).intersectsTimestampset(TimestampSet('{2019-09-04 00:00:00, 2019-09-05 00:00:00}')) == False
	assert TFloatI(expected).intersectsPeriod(Period('[2019-09-01 00:00:00, 2019-09-02 00:00:00]')) == True
	assert TFloatI(expected).intersectsPeriod(Period('(2019-09-01 00:00:00, 2019-09-02 00:00:00)')) == False
	assert TFloatI(expected).intersectsPeriod(Period('[2019-09-04 00:00:00, 2019-09-05 00:00:00]')) == False
	assert TFloatI(expected).intersectsPeriodset(PeriodSet('{[2019-09-01 00:00:00, 2019-09-02 00:00:00]}')) == True
	assert TFloatI(expected).intersectsPeriodset(PeriodSet('{(2019-09-01 00:00:00, 2019-09-02 00:00:00)}')) == False
	assert TFloatI(expected).intersectsPeriodset(PeriodSet('{[2019-09-04 00:00:00, 2019-09-05 00:00:00]}')) == False


@pytest.mark.parametrize('expected_tfloati', [
	'{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01}',
	# ('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
	# (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')),
	['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
	[TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
	 TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
def test_tfloati_constructor(cursor, expected_tfloati):
	params = [TFloatI(expected_tfloati)]
	cursor.execute('INSERT INTO tbl_tfloati (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tfloati WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	assert result == TFloatI(expected_tfloati)


@pytest.mark.parametrize('expected_tfloatseq', [
	'[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
	'Interp=Stepwise;[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
	# ('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
	# (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')),
	['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
	[TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'),
	 TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
def test_tfloatseq_constructor(cursor, expected_tfloatseq):
	params = [TFloatSeq(expected_tfloatseq)]
	cursor.execute('INSERT INTO tbl_tfloatseq (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tfloatseq WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	assert result == TFloatSeq(expected_tfloatseq)

@pytest.mark.parametrize('expected_tfloats', [
	'{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
	'Interp=Stepwise;{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
	['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'],
	#(['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'], True),
	[TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),
	 TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')],
])
def test_tfloats_constructor(cursor, expected_tfloats):
	params = [TFloatS(expected_tfloats)]
	cursor.execute('INSERT INTO tbl_tfloats (temp) VALUES (%s)', params)
	cursor.execute('SELECT temp FROM tbl_tfloats WHERE temp=%s', params)
	result = cursor.fetchone()[0]
	assert result == TFloatS(expected_tfloats)
