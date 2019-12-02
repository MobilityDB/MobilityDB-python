"""
import pytest

from MobilityDB import TBoolInst


@pytest.mark.parametrize('expected', [
	'false@2019-09-01',
	#'{true@2019-08-03, true@2019-08-05, false@2019-09-01}',
	#'[true@2019-08-03, true@2019-08-05, false@2019-09-01]',
	#'{[true@2019-08-03, true@2019-08-05, false@2019-09-01],[false@2019-09-03]}',
])
def test_tbool_should_round(cursor, expected):
	params = TBoolInst(expected)
	cursor.execute('INSERT INTO tbl_tboolinst (temp) VALUES (%s)' % params)
	cursor.execute('SELECT temp FROM tbl_tboolinst WHERE temp=%s' % params)
	result = cursor.fetchone()[0]
	assert result == TBoolInst(expected)
"""