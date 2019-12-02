"""
import pytest
from MobilityDB import TGEOGPOINT


@pytest.mark.parametrize('expected', [
	'point(1.0 1.0)@2019-09-01',
	'{point(1.0 2.0)@2019-08-03, point(1.1 2.1)@2019-08-05, point(1.2 2.2)@2019-09-01}',
	'[point(1.0 2.0)@2019-08-03, point(1.1 2.1)@2019-08-05, point(1.2 2.2)@2019-09-01]',
	'{[point(1.0 2.0)@2019-08-03, point(1.1 2.1)@2019-08-05, point(1.2 2.2)@2019-09-01],[point(1.5 2.9)@2019-09-03]}'
])
def test_tgeogpoint_should_round(cursor, expected):
	params = TGEOGPOINT(expected)
	cursor.execute('INSERT INTO tbl_tgeogpoint (tgeogpoint_col) VALUES (%s)' % params)
	cursor.execute('SELECT tgeogpoint_col FROM tbl_tgeogpoint WHERE tgeogpoint_col=%s' % params)
	result = cursor.fetchone()[0]
	assert result == TGEOGPOINT(expected)
"""