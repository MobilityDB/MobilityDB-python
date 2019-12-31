import pytest
from datetime import datetime, timedelta
from bdateutil.parser import parse
from MobilityDB import TimestampSet, Period, PeriodSet


@pytest.mark.parametrize('expected_timestampset', [
	'{2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01, 2019-09-11 00:00:00+01}',
	['2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'],
	[parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), parse('2019-09-11 00:00:00+01')],
	#('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'),
])
def test_timestampset_constructor(cursor, expected_timestampset):
	params = TimestampSet(expected_timestampset)
	print(params)
	cursor.execute("INSERT INTO tbl_timestampset (timetype) VALUES (%s)" % params)
	cursor.execute("SELECT timetype FROM tbl_timestampset WHERE timetype=%s" % params)
	result = cursor.fetchone()[0]
	print(result)
	print(TimestampSet(expected_timestampset))
	assert result == TimestampSet(expected_timestampset)

@pytest.mark.parametrize('expected_period', [
	'[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]',
	'[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)',
	'(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]',
	'(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)',
	['2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01'],
	['2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', False, True]
])
def test_period_constructor(cursor, expected_period):
	params = Period(expected_period)
	print(params)
	cursor.execute("INSERT INTO tbl_period (timetype) VALUES (%s)" % params)
	cursor.execute("SELECT timetype FROM tbl_period WHERE timetype=%s" % params)
	result = cursor.fetchone()[0]
	print(result)
	print(Period(expected_period))
	assert result == Period(expected_period)

@pytest.mark.parametrize('expected_periodset', [
	'{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]}',
	'{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01], [2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]}',
	['[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]', '[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]'],
	[Period('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]'), Period('[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]')],
])
def test_period_constructor(cursor, expected_periodset):
	params = PeriodSet(expected_periodset)
	print(params)
	cursor.execute("INSERT INTO tbl_periodset (timetype) VALUES (%s)" % params)
	cursor.execute("SELECT timetype FROM tbl_periodset WHERE timetype=%s" % params)
	result = cursor.fetchone()[0]
	print(result)
	print(PeriodSet(expected_periodset))
	assert result == PeriodSet(expected_periodset)
