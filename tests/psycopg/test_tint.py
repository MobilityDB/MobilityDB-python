"""
import pytest
from MobilityDB import TIntInst


@pytest.mark.parametrize('expected', [
	'10@2019-09-01',
	#'{8@2019-08-03, 13@2019-08-05, 10@2019-09-01}',
	#'[8@2019-08-03, 13@2019-08-05, 10@2019-09-01]',
	#'{[8@2019-08-03, 13@2019-08-05, 10@2019-09-01],[20@2019-09-03]}',
])
def test_tint_should_round(cursor, expected):
	params = TIntInst(expected)
	cursor.execute('INSERT INTO tbl_tintinst (temp) VALUES (%s)' % params)
	cursor.execute('SELECT temp FROM tbl_tintinst WHERE temp=%s' % params)
	result = cursor.fetchone()[0]
	assert result == TIntInst(expected)
"""