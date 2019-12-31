"""
import pytest
from MobilityDB import TGeogPoint


@pytest.mark.parametrize('expected', [
	'point(1.0 1.0)@2019-09-01',
	'{point(1.0 2.0)@2019-08-03, point(1.1 2.1)@2019-08-05, point(1.2 2.2)@2019-09-01}',
	'[point(1.0 2.0)@2019-08-03, point(1.1 2.1)@2019-08-05, point(1.2 2.2)@2019-09-01]',
	'{[point(1.0 2.0)@2019-08-03, point(1.1 2.1)@2019-08-05, point(1.2 2.2)@2019-09-01],[point(1.5 2.9)@2019-09-03]}'
])
def test_tgeogpoint_constructor(cursor, expected):
	params = TGeogPoint(expected)
	cursor.execute('INSERT INTO tbl_tgeogpoint (temp) VALUES (%s)' % params)
	cursor.execute('SELECT temp FROM tbl_tgeogpoint WHERE temp = %s' % params)
	result = cursor.fetchone()[0]
	assert result == TGeogPoint(expected)
"""