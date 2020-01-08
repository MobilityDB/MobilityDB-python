import pytest
from datetime import timedelta
from dateutil.parser import parse
from mobilitydb import TimestampSet, Period, PeriodSet


@pytest.mark.parametrize('expected_timestampset', [
	'{2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01, 2019-09-11 00:00:00+01}',
	['2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'],
	[parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), parse('2019-09-11 00:00:00+01')],
	('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'),
	(parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), parse('2019-09-11 00:00:00+01')),
])
def test_timestampset_constructor(cursor, expected_timestampset):
	if isinstance(expected_timestampset, tuple):
		params = TimestampSet(*expected_timestampset)
	else:
		params = TimestampSet(expected_timestampset)
	cursor.execute("INSERT INTO tbl_timestampset (timetype) VALUES (%s)" % params)
	cursor.execute("SELECT timetype FROM tbl_timestampset WHERE timetype=%s" % params)
	result = cursor.fetchone()[0]
	if isinstance(expected_timestampset, tuple):
		assert result == TimestampSet(*expected_timestampset)
	else:
		assert result == TimestampSet(expected_timestampset)

@pytest.mark.parametrize('expected_timestampset', [
	'{2019-09-01 00:00:00+01, 2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01}',
])
def test_TimestampSet_accessors(cursor, expected_timestampset):
	assert TimestampSet(expected_timestampset).timespan() == timedelta(2)
	assert TimestampSet(expected_timestampset).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert TimestampSet(expected_timestampset).numTimestamps() == 3
	assert TimestampSet(expected_timestampset).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert TimestampSet(expected_timestampset).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert TimestampSet(expected_timestampset).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert TimestampSet(expected_timestampset).timestamps() == \
		   [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'), parse('2019-09-03 00:00:00+01')]
	assert TimestampSet(expected_timestampset).shift(timedelta(days=1)) == \
		   TimestampSet('{2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01, 2019-09-04 00:00:00+01}')

@pytest.mark.parametrize('expected_period', [
	'[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]',
	'[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)',
	'(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]',
	'(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)',
	('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01'),
	('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', False, True),
	(parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01')),
	(parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), False, True),
])
def test_period_constructor(cursor, expected_period):
	if isinstance(expected_period, tuple):
		params = Period(*expected_period)
	else:
		params = Period(expected_period)
	cursor.execute("INSERT INTO tbl_period (timetype) VALUES (%s)" % params)
	cursor.execute("SELECT timetype FROM tbl_period WHERE timetype=%s" % params)
	result = cursor.fetchone()[0]
	if isinstance(expected_period, tuple):
		assert result == Period(*expected_period)
	else:
		assert result == Period(expected_period)

@pytest.mark.parametrize('expected_period', [
	'[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]',
])
def test_period_accessors(cursor, expected_period):
	assert Period(expected_period).lower() == parse('2019-09-01 00:00:00+01')
	assert Period(expected_period).upper() == parse('2019-09-03 00:00:00+01')
	assert Period(expected_period).lower_inc() == True
	assert Period(expected_period).upper_inc() == True
	assert Period(expected_period).timespan() == timedelta(2)
	assert Period(expected_period).shift(timedelta(days=1)) == Period('[2019-09-02 00:00:00+01, 2019-09-04 00:00:00+01]')

@pytest.mark.parametrize('expected_periodset', [
	'{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]}',
	'{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01], [2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]}',
	['[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]', '[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]'],
	[Period('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]'),
	 Period('[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]')],
	('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]', '[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]'),
	(Period('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]'),
	 Period('[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]')),
])
def test_periodset_constructor(cursor, expected_periodset):
	if isinstance(expected_periodset, tuple):
		params = PeriodSet(*expected_periodset)
	else:
		params = PeriodSet(expected_periodset)
	cursor.execute("INSERT INTO tbl_periodset (timetype) VALUES (%s)" % params)
	cursor.execute("SELECT timetype FROM tbl_periodset WHERE timetype=%s" % params)
	result = cursor.fetchone()[0]
	if isinstance(expected_periodset, tuple):
		assert result == PeriodSet(*expected_periodset)
	else:
		assert result == PeriodSet(expected_periodset)

@pytest.mark.parametrize('expected_periodset', [
	'{[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01],  [2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]}',
])
def test_PeriodSet_accessors(cursor, expected_periodset):
	assert PeriodSet(expected_periodset).timespan() == timedelta(2)
	assert PeriodSet(expected_periodset).period() == Period('[2019-09-01 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert PeriodSet(expected_periodset).numTimestamps() == 3
	assert PeriodSet(expected_periodset).startTimestamp() == parse('2019-09-01 00:00:00+01')
	assert PeriodSet(expected_periodset).endTimestamp() == parse('2019-09-03 00:00:00+01')
	assert PeriodSet(expected_periodset).timestampN(2) == parse('2019-09-02 00:00:00+01')
	assert PeriodSet(expected_periodset).timestamps() == \
		   [parse('2019-09-01 00:00:00+01'), parse('2019-09-02 00:00:00+01'), parse('2019-09-03 00:00:00+01')]
	assert PeriodSet(expected_periodset).numPeriods() == 2
	assert PeriodSet(expected_periodset).startPeriod() == Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]')
	assert PeriodSet(expected_periodset).endPeriod() == Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert PeriodSet(expected_periodset).periodN(2) == Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')
	assert PeriodSet(expected_periodset).periods() == [Period('[2019-09-01 00:00:00+01, 2019-09-01 00:00:00+01]'),
													   Period('[2019-09-02 00:00:00+01, 2019-09-03 00:00:00+01]')]
	assert PeriodSet(expected_periodset).shift(timedelta(days=1)) == \
		   PeriodSet('{[2019-09-02 00:00:00+01, 2019-09-02 00:00:00+01],  '
					 '[2019-09-03 00:00:00+01, 2019-09-04 00:00:00+01]}')


