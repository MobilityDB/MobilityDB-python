"""
import pytest

from MobilityDB import TBox


@pytest.mark.parametrize('expected', [
	'TBOX((10.0, 2019-09-08 00:00:00+02), (30.0, 2019-09-10 00:00:00+02))',
	'TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))',
	'TBOX((10.0, ), (30.0, ))'
])
def test_tint_should_round(cursor, expected):
	params = TBOX(expected)
	cursor.execute("INSERT INTO tbl_tbox (tbox_col) VALUES ('%s')" % params)
	cursor.execute("SELECT tbox_col FROM tbl_tbox WHERE tbox_col='%s'" % params)
	result = cursor.fetchone()[0]
	assert result == TBOX(expected)
"""